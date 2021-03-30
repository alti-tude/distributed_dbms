from DDBMS.Execution import DataTransfer
from DDBMS.DB import DBUtils, db


def executeCross(tables, cols, query_id, operation_id):
    with db.returnLists():
        data = DBUtils.crossQuery(*tables)
    DataTransfer.put(query_id, operation_id, data, cols, decode=False)
