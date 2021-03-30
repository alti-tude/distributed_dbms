#TODO remember to move all data to the initial site which received query

from DDBMS.Execution import Site
from DDBMS.Parser.SQLParser import *
from DDBMS.RATree.Nodes import *
from DDBMS import RATree
from DDBMS.DB import DBUtils
import Config
from treelib import Tree
import traceback
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

def setBestJoinSite(node, children_cols, children_rows):
    predicate_cols = node.join_predicate.getAllColumns()
    if len(predicate_cols) == 1:
        predicate_cols.append(predicate_cols[0])

    left_col = None
    right_col = None

    if predicate_cols[0] in children_cols[0]:
        left_col = predicate_cols[0]
        right_col = predicate_cols[1]
    else:
        left_col = predicate_cols[1]
        right_col = predicate_cols[0]
    
    left_benefit = SDDAlgorithm(left_col, children_rows[0], children_rows[1], children_cols[1])
    right_benefit = SDDAlgorithm(right_col, children_rows[1], children_rows[0], children_cols[0])

    if left_benefit >= right_benefit:
        node.site = node.children[0].site
        node.semijoin_transfer_col = left_col
        node.semijoin_transfer_child = 0
    else:
        node.site = node.children[1].site
        node.semijoin_transfer_col = right_col
        node.semijoin_transfer_child = 1

def getRowsAndExecutionSites(node):
    if isinstance(node, RelationNode):
        node.site = getFragmentSite(node.name)
        cols = SQLQuery.get().filterCols(table=node.table)
        return [1000000000, cols]

    children_cols = []
    children_rows = []
    for child in node.children:
        [child_rows, child_cols] = getRowsAndExecutionSites(child)
        children_rows.append(child_rows)
        children_cols.append(child_cols)

    children_cols_set = list(set([j for i in children_cols for j in i]))
    
    max_child_rows = max(children_rows)
    best_execution_site_idx = children_rows.index(max_child_rows)
    node.site = node.children[best_execution_site_idx].site

    if isinstance(node, SelectNode):
        predicate_selectivity = getPredicateSelectivity(node.predicate)
        return [max_child_rows * predicate_selectivity, children_cols_set]
    
    if isinstance(node, GroupbyNode):
        return [max_child_rows / 2, children_cols_set]

    if isinstance(node, UnionNode):
        return [sum(children_rows), children_cols_set]
    
    if isinstance(node, CrossNode):
        return [math.prod(children_rows), children_cols_set]

    if isinstance(node, ProjectNode) or isinstance(node, FinalProjectNode):
        return [max_child_rows, list(set(node.columns))]
    
    if isinstance(node, JoinNode):
        setBestJoinSite(node, children_cols, children_rows)
        return [math.prod(children_rows) * Config.SELECTIVITY_FACTOR, children_cols_set]

    return [max_child_rows, children_cols_set]

def buildTree(sql_query : str):
    SQLQuery.reset()
    parser = SQLParser()
    parser.parse(sql_query)
    root = RATree.optimise()

    if Config.DEBUG:
        tree = Tree()
        root.to_treelib(tree)
        tree.show()

    getRowsAndExecutionSites(root)         
    
    if Config.DEBUG:
        tree = Tree()
        root.to_treelib(tree)
        tree.show()
                
    return root

def execute(sql_query : str):
    pass
    # try:
    # except Exception as e:
    #     if Config.DEBUG:
    #         traceback.print_exc()
    #     print("An exception has occured. Please verify the query.")
