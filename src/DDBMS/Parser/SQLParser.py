import moz_sql_parser
from DDBMS.DB import db 
from DDBMS.Exceptions import SQLParserException

def parse_sql(query):
    query = query.replace('"', "'")
    try:
        return moz_sql_parser.parse(query)
    except Exception as e:
        raise SQLParserException(e)
