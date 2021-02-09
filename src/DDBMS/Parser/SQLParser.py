import moz_sql_parser
from DDBMS.DB import db 
from DDBMS.Exceptions import *
import DDBMS.DataStructures as DataStructures

def parse_sql(query):
    query = query.replace('"', "'")
    try:
        return moz_sql_parser.parse(query)
    except Exception as e:
        raise SQLParserException(e)


@db.execute
def get_schema():
    return "SELECT * FROM Attribute;"


def parse_select_attribute(column_name):
    column_details = column_name.split('.')
    
    if len(column_details) > 2:
        raise SQLVerifyException("Invalid query")
    elif len(column_details) == 1:
        return None, column_details[0]
    else:
        return column_details[0], column_details[1]


# Write this recursively for each select
def verify(query):
    if 'from' not in query:
        raise SQLVerifyException("No FROM clause found in query")

    schema = get_schema()
    application_relations = schema.RelationName.unique()

    alias_table_map = get_from_tables(application_relations, query['from'])
    print(alias_table_map)

    select_columns, select_all_present = get_select_columns(query['select']) 
    print(select_columns, select_all_present)

    verify_select_columns(select_columns, 
                          select_all_present,
                          alias_table_map,
                          schema[['RelationName', 'AttributeName']])

    # Do select_all_present logic


def get_from_tables(application_relations, from_query):
    from_tables = [from_query] if isinstance(from_query, str) else from_query
    table_alias = {} # Maps alias to actual name. Stores all tables

    for table in from_tables:
        relation_name = table
        if (
            isinstance(table, dict) and 
            'name' in table and 
            'value' in table and
            (table['name'] not in table_alias)
        ):
            table_alias[table['name']] = table['value']
            relation_name = table['value']
        elif isinstance(table, str) and table not in table_alias:
            table_alias[table] = table
        else:
            raise SQLVerifyException("Invalid query")

        if relation_name not in application_relations:
            raise SQLVerifyException("Invalid relation name", relation_name)
    
    return table_alias


def get_select_columns(select_query):
    select_all_present = False
    select_columns = []
    select_attrs = [select_query] if not isinstance(select_query, list) else select_query
    
    for attr in select_attrs:
        cur_column = DataStructures.Column(name=None, table=None)
        if attr == '*':
            select_all_present = True
        elif isinstance(attr, dict):
            cur_column.name = attr['value']
            
            if isinstance(attr['value'], dict):
                sql_aggr = next(iter(attr['value']))
                cur_column.aggregation = sql_aggr
                cur_column.name = attr['value'][sql_aggr]
            else:
                cur_column.aggregation = "none"

            if not isinstance(cur_column.name, str):
                raise SQLVerifyException("Invalid query")

            if 'name' in attr:
                cur_column.alias = attr['name']

            cur_column.table, cur_column.name = parse_select_attribute(cur_column.name)
            select_columns.append(cur_column)
        else:
            raise SQLVerifyException("Invalid query")

    return select_columns, select_all_present


def verify_select_columns(select_columns, select_all_present, alias_table_map, schema):
    for i, col in enumerate(select_columns):
        col_table = None
        col_alias = None

        if col.table is None:
            for j, row in schema.iterrows():
                relation = row['RelationName']
                attr = row['AttributeName']
      
                if attr == col.name and relation in alias_table_map:
                    if col_table is not None:
                        raise SQLVerifyException("Column(s) belong to multiple tables")
                    col_alias = relation
                    col_table = alias_table_map[col_alias]

        elif col.table in alias_table_map:
            col_alias = col.table
            col_table = alias_table_map[col_alias]

        if col_table is None:
            raise SQLVerifyException("Invalid column(s)")

        select_columns[i].table = DataStructures.Table(name=col_table, alias=col_alias)

    return select_columns


