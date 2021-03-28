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

from DDBMS.Execution.Execute import execute
from pprint import PrettyPrinter 

pp = PrettyPrinter(indent=2, compact=True)

# query = "select ScreenID from Screen, Theater where Screen.TheaterID = Theater.TheaterID and Theater.Location = 'Delhi';"
# query = "select TheaterID from Screen where TheaterID=1;"

while True:
    query = input("> ")
    execute(query)