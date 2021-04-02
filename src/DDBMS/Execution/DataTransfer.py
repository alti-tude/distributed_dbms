import traceback
from pandas.core.frame import DataFrame
from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.DB.DBUtils import createTable, dropTable, insertIntoTable, renameTable, selectQuery, tableExists
from DDBMS.DB import db
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Execution.Site import Site
import Config
from . import Routes

from typing import List
import pandas as pd
import pickle
import base64
import requests
import time

def getTempTableName(query_id, operation_id):
    if Config.LOCAL_SERVERS:
        return f"{query_id}_{operation_id}_{Site.CUR_SITE.name}"
    else:
        return f"{query_id}_{operation_id}"

def encodeFn(data):
    binary = pickle.dumps(data, fix_imports=True)
    return base64.b64encode(binary).decode('ascii')

def decodeFn(data : str):
    binary = base64.b64decode(data.encode('ascii'))
    return pickle.loads(binary, fix_imports=True)

def send(site : Site, query_id, operation_id, columns : List[Column], data = None):
    if data is None:
        with db.returnLists():
            data = selectQuery(columns, Table(getTempTableName(query_id, operation_id)))

    payload = {
        "query_id": query_id,
        "operation_id": operation_id,
        "data": encodeFn(data),
        "columns": encodeFn(columns)
    }

    url = f"{site.getUrl()}{Routes.INTERNAL.PUT}"
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(response.text)

def put(query_id, operation_id, data, columns, nameFn = None, decode = True):
    table_name = getTempTableName(query_id, operation_id)
    if decode:
        data = decodeFn(data)
        columns = decodeFn(columns)

    if isinstance(data, pd.DataFrame):
        raise Exception()

    if Config.DEBUG:
        print("[put]", query_id, operation_id)
        print("[put]", data)
        print("[put]", columns)

    if nameFn is None:
        nameFn = lambda col : f"{col.temp_name}"

    dropTable(table_name + "_tmp")
    createTable(table_name + "_tmp", columns, [nameFn(col) for col in columns])
    insertIntoTable(table_name + "_tmp", data)
    renameTable(table_name + "_tmp", table_name)

    return Table(table_name)
    
def get(query_id, operation_id):
    if Config.DEBUG: print(f"[GET]: {operation_id}")
    table_name = getTempTableName(query_id, operation_id)

    while not tableExists(table_name):
        time.sleep(Config.GET_RETRY_DELAY)

    return Table(table_name)