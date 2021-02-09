import argparse
from DDBMS.DB import DB

LOCAL_CONFIG = {
    "user": "ddbms2",
    "password": "ddbms",
    "host": "localhost",
    "database": "ddbms"
}

SERVER_CONFIG = {
    "user": "Samosa",
    "password": "Samose",
    "host": "localhost",
    "database": "Samosa",
    "auth_plugin": "mysql_native_password"
}

db = DB(config=LOCAL_CONFIG)

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



