import argparse
import mysql.connector


LOCAL_CONFIG = {
    "user": "ddbms",
    "password": "ddbms",
    "host": "localhost",
    "database": "ddbms"
}

SERVER_CONFIG = {
    "user": "Samosa",
    "password": "Samose",
    "host": "localhost",
    "database": "Samosa"
}

class DB:
    def __init__(self, *, user = "Samosa", password = "Samose", host = "127.0.0.1", database = "Samose"):
        self.config = {
            "user": user,
            "password": password,
            "host": host,
            "database": database
        }

    def execute(self, query_function):
        def wrapper(*args, **kwargs):
            conn = mysql.connector.connect(**self.config)
            cur = conn.cursor()
            
            query = query_function(*args, **kwargs)
            assert(isinstance(query,str))

            cur.execute(query)
            result = [item for item in cur]

            cur.close()
            conn.close()

            return result
        
        return wrapper
db = DB()

@db.execute
def getFragments(relation_name):
    query = f"CALL getFragments('{relation_name}');"
    return query

@db.execute
def getSites(fragment_name):
    query = f"CALL getSites('{fragment_name}');"
    return query    

parser = argparse.ArgumentParser()
parser.add_argument("--get-fragments", dest='method', default=argparse.SUPPRESS, action='store_const', const = getFragments)
parser.add_argument("--get-sites", dest='method', default=argparse.SUPPRESS, action='store_const', const = getSites)
parser.add_argument("--server-config", dest='config', default=LOCAL_CONFIG, action='store_const', const=SERVER_CONFIG)
parser.add_argument("key", type=str)
args = parser.parse_args()

if not args.method:
    parser.error("select atleast 1 query")

db.config = args.config
print(args.method(args.key))



