import moz_sql_parser
from DDBMS.DB import db 
from DDBMS.Exceptions import *

def parseSql(query):
    query = query.replace('"', "'")
    try:
        return moz_sql_parser.parse(query)
    except Exception as e:
        raise SQLParserException(e)


@db.execute
def get_schema():
    return "SELECT * FROM Attribute;"


# Write this recursively for each select
def verify(query):
    if 'from' not in query:
        raise SQLVerifyException("Incorrect query, no from clause found in query")

    schema = get_schema()
    application_relations = schema.RelationName.unique()

    table_alias = {} # Maps alias to actual name. Stores all tables
    for table in query['from']:
        if (
            type(table) is dict and 
            'name' in table and 
            'value' in table and
            (table['name'] not in table_alias)
        ):
            table_alias[table['name']] = table['value']
        elif type(table) is str and table not in table_alias:
            table_alias[table] = table
        else:
            raise SQLVerifyException("Invalid query")

    print(table_alias)