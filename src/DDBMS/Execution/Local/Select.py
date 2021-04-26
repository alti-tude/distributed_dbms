from DDBMS.Execution import DataTransfer
from Config import DEBUG
from DDBMS.Parser.SQLQuery.Predicate import Predicate
from DDBMS.RATree.Nodes import FinalProjectNode, GroupbyNode, ProjectNode, RelationNode, SelectNode
from DDBMS.RATree import Node
from DDBMS.DB import DBUtils, db
from DDBMS.Parser.SQLQuery.Symbols import PredicateOps

def executeSelect(root : Node, query_id, operation_id):
    if isinstance(root, GroupbyNode):
        return

    if isinstance(root, RelationNode):
        return root.table

    predicates = []
    cur_node = root
    
    cols = None
    col_temp_names = []

    while not isinstance(cur_node, RelationNode):
        if isinstance(cur_node, ProjectNode) or isinstance(cur_node, FinalProjectNode):
            if cols is None:
                cols = cur_node.cols
            print("TEMP NAMES:", cols)
            print(cur_node.columns)

        if isinstance(cur_node, SelectNode):
            predicates.append(cur_node.predicate)
        
        cur_node = cur_node.children[0]

    table = cur_node.table
    predicate = Predicate(PredicateOps.AND, operands=predicates)

    if DEBUG:
        with db.returnStrings():
            print(DBUtils.selectQuery(cols, table, predicate))
    
    with db.returnLists():
        data = DBUtils.selectQuery(cols, table, predicate)
    return DataTransfer.put(query_id, operation_id, data, cols, decode=False)