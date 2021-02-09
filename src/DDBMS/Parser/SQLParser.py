import moz_sql_parser
from DDBMS.DB import db 
from DDBMS.Exceptions import SQLParserException

class SQLParser:
    def __init__(self):
        pass

    def sql_parse(self, query):
        try:
            return moz_sql_parser.parse(query)
        except Exception as e:
            raise SQLParserException(e)
