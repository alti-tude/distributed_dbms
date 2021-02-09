from moz_sql_parser import parse
from DDBMS.DB import db 

class SQLParser:
    def __init__(self):
        pass

    def sql_to_json(self, query):
        # return json.dumps(parse(query), indent=2)
        return parse(query)
