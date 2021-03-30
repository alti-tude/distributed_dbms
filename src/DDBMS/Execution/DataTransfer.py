from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.DB.DBUtils import createTable, dropTable, insertIntoTable, tableExists
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Execution.Site import Site
import Config
from Api import Routes

from typing import List
import pandas as pd
import pickle
import base64
import requests
import time

def getTempTableName(query_id, operation_id):
    return f"{query_id}_{operation_id}"

def encode(data):
    binary = pickle.dumps(data, fix_imports=True)
    return base64.b64encode(binary).decode('ascii')

def decode(data : str):
    binary = base64.b64decode(data.encode('ascii'))
    return pickle.loads(binary, fix_imports=True)

def send(site : Site, query_id, operation_id, data : pd.DataFrame, columns = List[Column]):
    payload = {
        "query_id": query_id,
        "operation_id": operation_id,
        "data": encode(data),
        "columns": encode(columns)
    }

    url = f"{site.getUrl()}{Routes.INTERNAL.PUT}"
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(response.text)

def put(query_id, operation_id, data, columns):
    table_name = getTempTableName(query_id, operation_id)
    data = decode(data)
    columns = decode(columns)

    if Config.DEBUG:
        print(data)
        print(columns)

    dropTable(table_name)
    createTable(table_name, columns, [f"{col.name}_{col.alias}" for col in columns])
    insertIntoTable(table_name, data)
    
def get(query_id, operation_id):
    table_name = getTempTableName(query_id, operation_id)

    while not tableExists(table_name):
        time.sleep(Config.GET_RETRY_DELAY)

    return Table(table_name)