import datetime

from Config import DEBUG
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
    if DEBUG: print("="*20, table_name, col_names)
    cols = ','.join([f"{col_name} {col.data_type} " for col_name, col in zip(col_names, columns)])
    return f"create table `{table_name}` ({cols});"

@db.execute_commit
def renameTable(oname, nname):
    return f"rename table `{oname}` to `{nname}`;"

@db.execute_commit
def insertIntoTable(table_name, data, columns = None):
    if isinstance(data, pd.DataFrame):
        data = data.values.tolist()

    if len(data) == 0:
        return f"select * from `{table_name}`;"

    def formatRow(row):
        template = []
        for i, elem in enumerate(row):
            if isinstance(elem, str):
                template.append(f"'{elem}'")
            elif isinstance(elem, datetime.date):
                template.append(f"'{elem.isoformat()}'")
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

@db.execute
def selectQuery(project_cols, from_table, where_predicate=None, group_by_cols = None, having_predicate = None):
    if len(project_cols)==0:
        project_cols_str = "*"
    else:
        project_cols_str = ""
        for col in project_cols:
            if project_cols_str != "":
                project_cols_str += ", "
            if isinstance(col, str): 
                project_cols_str += col
            elif col.aggregation != "none":
                project_cols_str += col.aggregation + "(" + col.temp_name + ")"
            else:
                project_cols_str += col.temp_name
    
    from_table_str = from_table.name
    base_query = "SELECT " + project_cols_str + " FROM `" + from_table_str + "`"
    
    if where_predicate is not None and len(where_predicate.operands)!=0:
        where_predicate_str = where_predicate.compact_display()
        base_query = base_query + " WHERE " + where_predicate_str

    if group_by_cols is not None:
        group_by_cols_str = ""
        for col in group_by_cols:
            if group_by_cols_str != "":
                group_by_cols_str += ", "
            if isinstance(col, str): 
                group_by_cols_str += col
            else:
                group_by_cols_str += col.temp_name

        base_query += f" GROUP BY {group_by_cols_str}"
    
    if having_predicate is not None and len(having_predicate.operands) != 0:
        having_predicate_str = having_predicate.compact_display()
        base_query += f" HAVING {having_predicate_str}"
        
    return base_query + ";"

@db.execute
def join(table1, table2, col1, col2):
    return f"SELECT * FROM `{table1.name}`, `{table2.name}` WHERE `{table1.name}`.{col1.temp_name} = `{table2.name}`.{col2.temp_name};"

@db.execute
def semijoinQuery(table, col_as_table, col1, col2):
    return f"SELECT DISTINCT `{table.name}`.* FROM `{table.name}`, `{col_as_table.name}` WHERE `{table.name}`.{col1.temp_name} = `{col_as_table.name}`.{col2.temp_name};"

@db.execute
def unionQuery(tables):
    sql_query = ""
    for table in tables:
        if sql_query != "":
            sql_query += " UNION ALL "
        sql_query += "SELECT * FROM `" + table.name + "`"
    return sql_query + ";"

@db.execute
def crossQuery(table1, table2):
    return "SELECT * FROM `" + table1.name + "`, `" + table2.name + "`;"


@db.execute_commit
def directExecuteCommit(query):
    return query

@db.execute
def directExecute(query):
    return query