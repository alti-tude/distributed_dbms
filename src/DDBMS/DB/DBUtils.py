import pandas as pd
from typing import List
from DDBMS.DB import db

@db.execute
def queryFragmentSite(fragment_name):
    return "SELECT SiteID FROM LocalMapping WHERE FragmentID = '" + fragment_name + "';"

@db.execute
def getDataType(attribute_name, table_name):
    query = f"select DataType from Attribute where AttributeName = '{attribute_name}' and RelationName = '{table_name}'"
    return query

@db.execute
def getTableLike(table_name):
    return f"show tables like '{table_name}';"

def tableExists(table_name):
    return len(getTableLike(table_name)) != 0

@db.execute_commit
def dropTable(table_name):
    return f"drop table if exists `{table_name}`;"

@db.execute_commit
def createTable(table_name, columns, col_names : List[str]):
    cols = ','.join([f"{col_name} {col.data_type} " for col_name, col in zip(col_names, columns)])
    return f"create table `{table_name}` ({cols});"

@db.execute_commit
def insertIntoTable(table_name, data, columns = None):
    if isinstance(data, pd.DataFrame):
        data = data.values.tolist()
    
    
    def formatRow(row):
        template = []
        for i, elem in enumerate(row):
            if isinstance(elem, str):
                template.append(f"'{elem}'")
            else:
                template.append(f"{elem}")
        
        return ', '.join(template)

    values = ', '.join([f"({formatRow(row)})" for row in data])

    if columns is None:
        query = f"insert into `{table_name}` values {values};"
    else:
        cols = ', '.join([col.name for col in columns])
        query = f"insert into `{table_name}`({cols}) values {values};"
    
    return query