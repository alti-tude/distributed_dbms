import moz_sql_parser
from DDBMS.Parser.SQLQuery import *

def parseSQL(query):
    query = query.replace('"', "'")
    return moz_sql_parser.parse(query)


def formatParsedQuery(query):
    formatted_query = SQLQuery()
    addFromTables(query, formatted_query)
    print(formatted_query.tables)


def addFromTables(query, formatted_query):
    from_query = query['from']
    from_tables = [from_query] if not isinstance(from_query, list) else from_query

    for table in from_tables:
        if isinstance(table, dict):
            formatted_query.addFrom(Table(table['value'], table['name']))
        else:
            formatted_query.addFrom(Table(table))

