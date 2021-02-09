import moz_sql_parser
from DDBMS.DB import db 
from DDBMS.Exceptions import *

def parse_sql(query):
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
        raise SQLVerifyException("No FROM clause found in query")

    schema = get_schema()
    application_relations = schema.RelationName.unique()

    from_tables = [query['from']] if isinstance(query['from'], str) else query['from']
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

    print(table_alias)

    