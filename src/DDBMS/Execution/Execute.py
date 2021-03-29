#TODO remember to move all data to the initial site which received query

from DDBMS.RATree.Transformations.CombineSelectAndCross import CombineSelectAndCross
from DDBMS.RATree.Transformations.reduceHorizontalFrag import reduceHorizontalFrag
from DDBMS.RATree.Transformations.reduceDerivedHorizontalFrag import reduceDerivedHorizontalFrag
from DDBMS.RATree.Transformations.Localise import materialiseAllTables, materialiseTable
from DDBMS.RATree.Transformations.MoveUnionUp import moveUnionUp, __moveUnionUpStep
from DDBMS.RATree.Transformations.PushProject import pushProject
from DDBMS.RATree.Transformations.PushSelect import pushSelect
from DDBMS.Parser.SQLParser import *
from DDBMS.RATree.Nodes import *
from DDBMS.RATree import RATreeBuilder
from pprint import PrettyPrinter 
import Config
from treelib import Tree
import traceback
from DDBMS.DB import db

@db.execute
def queryFragmentSite(fragment_name):
    return "SELECT SiteID FROM LocalMapping WHERE FragmentID = '" + fragment_name + "';"

@db.execute
def getApplicationSchema(relation_name):
    return "SELECT DataType FROM Attribute WHERE RelationName = '"+ relation_name +"';"

def getFragmentSite(fragment_name):
    result = queryFragmentSite(fragment_name)
    return result['SiteID'].iloc[0]

def getDataTypeSize(datatype):
    datatype_size = {'INT':4, 'DATETIME':8, 'DATE':3, 'TINYTEXT':256, 'TEXT':65535, 'MEDIUMTEXT':16777215, 'LONGTEXT': 4294967295}
    if datatype in datatype_size:
        return datatype_size[datatype]
    elif datatype[0:7] == 'VARCHAR':
        return int(datatype[8:-1]) + 2
    return 4

def execute(sql_query : str):
    try:
        SQLQuery.reset()
        root = getRATree(sql_query)
        tree = Tree()
        root.to_treelib(tree)
        tree.show()
        getRowsAndExecutionSites(root) 
    except Exception as e:
        if Config.DEBUG:
            traceback.print_exc()
        print("An exception has occured. Please verify the query.")

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
    
def getRowsAndExecutionSites(node):
    if isinstance(node, RelationNode):
        node.site = getFragmentSite(node.name)
        return 1000000000

    max_child_rows = 0
    total_child_rows = 0
    prod_child_rows = 1
    best_execution_site = None
    for child in node.children:
        child_rows = getRowsAndExecutionSites(child)
        total_child_rows += child_rows
        prod_child_rows *= child_rows
        if child_rows >= max_child_rows:
            max_child_rows = child_rows
            best_execution_site = child.site
    
    node.site = best_execution_site

    if isinstance(node, SelectNode):
        predicate_selectivity = getPredicateSelectivity(node.predicate)
        return max_child_rows * predicate_selectivity
    
    if isinstance(node, GroupbyNode):
        return max_child_rows / 2

    if isinstance(node, UnionNode):
        return total_child_rows
    
    if isinstance(node, CrossNode):
        return prod_child_rows
    
    if isinstance(node, JoinNode):
        return prod_child_rows * Config.SELECTIVITY_FACTOR

    return max_child_rows

def getRATree(query : str):
    parser = SQLParser()
    parser.parse(query)

    ra_tree = RATreeBuilder()
    root = ra_tree.projected
    root = pushSelect(ra_tree.projected)

    tree = Tree()
    root.to_treelib(tree)
    tree.show()
    root = CombineSelectAndCross(root)
    root = pushProject(root)

    #? Materialise handles reduce vertical
    
    root = materialiseAllTables(root)
    root = pushSelect(root)
    root = pushProject(root)
    root = moveUnionUp(root)
    root = reduceHorizontalFrag(root)

    root = pushSelect(root)
    root = pushProject(root)
    root = reduceDerivedHorizontalFrag(root)

    root = pushSelect(root)
    root = pushProject(root)

    return root