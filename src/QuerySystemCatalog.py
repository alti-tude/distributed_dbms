import argparse
from DDBMS.DB import db
import Config

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
parser.add_argument("--server-config", dest='config', default=Config.LOCAL_DB_CONFIG, action='store_const', const=Config.SERVER_DB_CONFIG)
parser.add_argument("key", type=str)
args = parser.parse_args()

if not args.method:
    parser.error("select atleast 1 query")

db.config = args.config
print(args.method(args.key))



