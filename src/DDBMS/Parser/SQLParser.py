import moz_sql_parser
from DDBMS.DB import db 

class SQLParser:
    def __init__(self):
        pass

    def sql_parse(self, query):
        return moz_sql_parser.parse(query)
