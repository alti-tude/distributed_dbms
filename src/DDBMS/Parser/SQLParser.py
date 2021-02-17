import moz_sql_parser
from DDBMS.Parser.SQLQuery import *

class SQLParser:
    def __init__(self):
        self.formatted_query = SQLQuery()

    def reset(self):
        self.formatted_query.reset()


    def parse(self, original_query):
        query = original_query.replace('"', "'")
        query = moz_sql_parser.parse(query)

        self.addFromTables(query)
        print(self.formatted_query.tables)

        self.reset()


    def addFromTables(self, query):
        from_query = query['from']
        from_tables = [from_query] if not isinstance(from_query, list) else from_query

        for table in from_tables:
            if isinstance(table, dict):
                self.formatted_query.addFrom(Table(table['value'], table['name']))
            else:
                self.formatted_query.addFrom(Table(table))

    


