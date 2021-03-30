from DDBMS.RATree import Node
from DDBMS.DB import DBUtils, db
from DDBMS.Execution import DataTransfer

def executeUnion(tables, cols, query_id, operation_id):
    print(__name__, tables)
    with db.returnLists():
        data = DBUtils.unionQuery(tables)

    # scols = sorted(cols, key=lambda elem : elem.name)
    return DataTransfer.put(query_id, operation_id, data, cols, decode=False)

