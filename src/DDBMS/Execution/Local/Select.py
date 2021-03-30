from DDBMS.Execution import DataTransfer
from DDBMS.Parser.SQLQuery.Table import Table
from Config import DEBUG
from DDBMS.Parser.SQLQuery.Predicate import Predicate
from DDBMS.RATree.Nodes import FinalProjectNode, ProjectNode, RelationNode, SelectNode
from DDBMS.RATree import Node
from DDBMS.DB import DBUtils, db
from DDBMS.Parser.SQLQuery.Symbols import PredicateOps
from DDBMS.Execution.DataTransfer import getTempTableName

def executeSelect(root : Node, query_id, operation_id, cols=[]):
    if isinstance(root, RelationNode):
        return root.table

    print(__name__, root)
    predicates = []
    cur_node = root
    
    while not isinstance(cur_node, RelationNode):
        if isinstance(cur_node, ProjectNode) or isinstance(cur_node, FinalProjectNode):
            for col in cur_node.cols:
                if col not in cols:
                    cols.append(col)
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