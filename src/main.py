from DDBMS.Execution import Site
from DDBMS.Execution.DataTransfer import get, send
from numpy import insert
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.DB import db
from DDBMS.DB.DBUtils import *

@db.execute
def test():
    return "select * from LocalMapping;"

print(test())
columns = [
    Column("MovieId", alias="id", table=Table("Movie")),
    Column("Location", alias="loc", table=Table("Theater")),
    Column("Price", table=Table("Show"))
]

col_names = ["id", "loc", "price"]

data = {
    "id": [1,2],
    "loc": ["loc1", "loc2"],
    "price": [10.0201, 11]
}

data = pd.DataFrame(data)

send(Site("hyderabad", "localhost", 12345),"quid", "oid", data, columns)
# print(get("quid", "oid"))
# from DDBMS.DataStructures.Table import Table
# from DDBMS.DataStructures.Predicate import getPredicateObj
# from DDBMS.DataStructures.Column import Column
# from DDBMS.DataStructures.Symbols import Keywords

# predicate = {
#     'select': [Column(name="id", table="t1")],
#     'from': [Table(name="t1")],
#     'where': {'and': [
#         {'gt': [Column(name="id", table="t1"), 3]},
#         {'eq': [Column(name="a", table="t1"), Column(name="b", table="t2")]},
#         {'eq': [Column(name="c", table="t1"), Column(name="b", table="t2")]},
#     ]}
# }

# print(getPredicateObj(predicate))

# from DDBMS.Execution.Execute import buildTree
# from pprint import PrettyPrinter 

# pp = PrettyPrinter(indent=2, compact=True)

# # query = "select ScreenID from Screen, Theater where Screen.TheaterID = Theater.TheaterID and Theater.Location = 'Delhi';"
# # query = "select TheaterID from Screen where TheaterID=1;"

# while True:
#     query = input("> ")
#     buildTree(query)
