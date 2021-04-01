from DDBMS.RATree.Nodes import RelationNode
from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.RATree import Node
from DDBMS.DB import DBUtils, db
from DDBMS.Execution import DataTransfer

def executeUnion(cur_node, query_id, operation_id):
    child_tables = [Table(DataTransfer.getTempTableName(query_id, child.operation_id)) for child in cur_node.children]
    for i in range(len(child_tables)):
        if isinstance(cur_node.children[i], RelationNode):
            child_tables[i] = cur_node.children[i].table
    
    with db.returnLists():
        data = DBUtils.unionQuery(child_tables)

    # scols = sorted(cols, key=lambda elem : elem.name)
    return DataTransfer.put(query_id, operation_id, data, cur_node.cols, decode=False)

