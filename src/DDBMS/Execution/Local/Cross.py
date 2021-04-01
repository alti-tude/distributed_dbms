from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.RATree.Nodes import RelationNode
from DDBMS.Execution import DataTransfer
from DDBMS.DB import DBUtils, db


def executeCross(cur_node, query_id, operation_id):
    child_tables = [Table(DataTransfer.getTempTableName(query_id, child.operation_id)) for child in cur_node.children]
    for i in range(len(child_tables)):
        if isinstance(cur_node.children[i], RelationNode):
            child_tables[i] = cur_node.children[i].table
    
    with db.returnLists():
        data = DBUtils.crossQuery(child_tables[0], child_tables[1])
    DataTransfer.put(query_id, operation_id, data, cur_node.cols, decode=False)
