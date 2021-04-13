from DDBMS.Execution.DataTransfer import getTempTableName
from numpy import isin
from .Site import Site
from DDBMS.Parser.SQLParser import *
from DDBMS.RATree.Nodes import *
from DDBMS import RATree
from DDBMS.DB import DBUtils
import Config
from treelib import Tree
import math

def getFragmentSite(fragment_name):
    result = DBUtils.queryFragmentSite(fragment_name)
    return Site(result['SiteID'].iloc[0])

def getDataTypeSize(datatype):
    datatype_size = {'INT': 4, 'DATETIME': 8, 'DATE': 3, 'TINYTEXT': 256,
                    'TEXT': 65535, 'MEDIUMTEXT': 16777215, 'LONGTEXT': 4294967295}
                    
    if datatype in datatype_size:
        return datatype_size[datatype]
    elif datatype[0:7] == 'VARCHAR':
        return int(datatype[8:-1]) + 2
    return 4

def getPredicateSelectivity(predicate):
    if predicate.operator == PredicateOps.OR or predicate.operator == PredicateOps.NOT:
        final_selectivity = 1
        for subpredicate in predicate.operands:
            pred_selectivity = getPredicateSelectivity(subpredicate)
            final_selectivity *= (1 - pred_selectivity)
        if predicate.operator == PredicateOps.NOT:
            return final_selectivity
        return 1 - final_selectivity
    
    if predicate.operator == PredicateOps.EQ:
        return Config.SELECTIVITY_FACTOR
    elif predicate.operator == PredicateOps.NEQ:
        return (1 - Config.SELECTIVITY_FACTOR)
    return (1 - Config.SELECTIVITY_FACTOR) * 0.5

def SDDAlgorithm(col : Column, col_rows, table_rows, table_cols : List[Column]):
    col_datatype = col.data_type
    col_datatype_size = getDataTypeSize(col_datatype)
    cost = col_datatype_size * col_rows

    table_datatypes_size = 0
    for table_col in table_cols:
        table_col_datatype = table_col.data_type
        table_datatypes_size += getDataTypeSize(table_col_datatype)

    benefit = (Config.SELECTIVITY_FACTOR) * table_datatypes_size * table_rows

    return -(benefit + cost)

def setBestJoinSite(node, children_cols, children_rows, query_id):
    ccols = [[SQLQuery.get().copyCol(col) for col in elem] for elem in children_cols]

    predicate_cols = node.join_predicate.getAllColumns()
    if len(predicate_cols) == 1:
        predicate_cols.append(predicate_cols[0])

    left_col = None
    right_col = None

    if predicate_cols[0] in ccols[0]:
        left_col = predicate_cols[0]
        right_col = predicate_cols[1]
    else:
        left_col = predicate_cols[1]
        right_col = predicate_cols[0]
    
    left_benefit = SDDAlgorithm(left_col, children_rows[0], children_rows[1], ccols[1])
    right_benefit = SDDAlgorithm(right_col, children_rows[1], children_rows[0], ccols[0])

    if left_benefit < right_benefit:
        node.children = list(reversed(node.children))
        ccols = list(reversed(ccols))
        left_benefit, right_benefit = right_benefit, left_benefit
        left_col, right_col = right_col, left_col

    node.child_temp_tables = [Table(getTempTableName(query_id, child.operation_id)) for child in node.children]
    node.child_sites = [child.site for child in node.children]
    node.site = node.child_sites[0]
    node.predicate_cols = [left_col, right_col]
    # ccols[1].pop(ccols[1].index(right_col))
    node.cols = ccols[0] + ccols[1]
    

def tempNameCols(node, predicate : Predicate):
    for i, operand in enumerate(predicate.operands):
        if isinstance(operand, Column):
            idx = node.cols.index(operand)
            predicate.operands[i] = node.cols[idx]
        if isinstance(operand, Predicate):
            tempNameCols(operand)


operation_id = 0
def getRowsAndExecutionSites(node, query_id):
    global operation_id
    node.operation_id = str(operation_id)
    print("="*40, type(node), operation_id)
    
    if isinstance(node, RelationNode):
        node.site = getFragmentSite(node.name)
        cols = SQLQuery.get().filterCols(table=node.table)
        cols = [SQLQuery.get().copyCol(col) for col in cols]
        for col in cols:
            col.temp_name = col.name
        node.cols = sorted(cols, key = lambda elem : elem.name)
        return [1000000000, node.cols]

    children_cols = []
    children_cols_not_flattened = []
    children_rows = []
    for child in node.children:
        operation_id += 1
        [child_rows, child_cols] = getRowsAndExecutionSites(child, query_id)
        children_rows.append(child_rows)
        children_cols_not_flattened.append(child_cols)
        for col in child_cols:
            if col not in children_cols:
                children_cols.append(col)
    
    max_child_rows = max(children_rows)
    best_execution_site_idx = children_rows.index(max_child_rows)
    node.site = node.children[best_execution_site_idx].site
    node.cols = children_cols

    num_rows = max_child_rows
        
    if isinstance(node, SelectNode):
        tempNameCols(node, node.predicate)
        predicate_selectivity = getPredicateSelectivity(node.predicate)
        num_rows = max_child_rows * predicate_selectivity
    
    if isinstance(node, GroupbyNode):
        num_rows = max_child_rows / 2

    if isinstance(node, FinalProjectNode):
        node.cols = []
        
        # for col in children_cols:
        #     if col in node.columns:
        #         node.cols.append(col)

        for col in node.columns:
            aggregation = col.aggregation
            col.aggregation = Aggregation.NONE
            child_col_idx = children_cols.index(col)
            col.temp_name = children_cols[child_col_idx].temp_name
            col.aggregation = aggregation
            node.cols.append(col)

        num_rows = max_child_rows
    
    if isinstance(node, ProjectNode):
        node.cols = []
        
        for col in children_cols:
            if col in node.columns:
                node.cols.append(col)

        num_rows = max_child_rows

    if isinstance(node, UnionNode):
        num_rows = sum(children_rows)

    if isinstance(node, CrossNode):
        num_rows = math.prod(children_rows)
    
    if isinstance(node, JoinNode):
        tempNameCols(node, node.join_predicate)
        setBestJoinSite(node, children_cols_not_flattened, children_rows, query_id)
        num_rows = math.prod(children_rows) * Config.SELECTIVITY_FACTOR
    
    if isinstance(node, (UnionNode, CrossNode, JoinNode)):
        node.cols = [SQLQuery.get().copyCol(col) for col in node.cols]

        col_map = {}
        for col in node.cols:
            name = f"{col.table.name}_{col.name}"
            if name in col_map:
                col_map[name].append(col)
            else:
                col_map[name] = [col]
        
        for name in col_map:
            for i, col in enumerate(col_map[name]):
                col.temp_name = f"{col.table.name}_{col.name}_{i}"
        

    return [num_rows, node.cols]

def buildTree(sql_query : str, query_id):
    global operation_id
    SQLQuery.reset()
    parser = SQLParser()
    parser.parse(sql_query)
    root = RATree.optimise()

    if Config.DEBUG:
        tree = Tree()
        root.to_treelib(tree)
        tree.show()

    operation_id = 0
    getRowsAndExecutionSites(root, query_id)         
    
    if Config.DEBUG:
        tree = Tree()
        root.to_treelib(tree)
        tree.show()
                
    return root
