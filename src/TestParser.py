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


from DDBMS.Parser.SQLParser import *
from DDBMS.RATree import RATreeBuilder
from pprint import PrettyPrinter 
from DDBMS.RATree.Transformations import *

pp = PrettyPrinter(indent=2, compact=True)

query = input()
parser = SQLParser()
sql_query = parser.parse(query)
# print(sql_query)

ra_tree = RATreeBuilder(sql_query)
pp.pprint(ra_tree.projected.to_dict())
ra_tree = pushSelect(ra_tree)
pp.pprint(ra_tree.projected.to_dict())

ra_tree = pushProject(ra_tree)
pp.pprint(ra_tree.projected.to_dict())

# from DDBMS.RATree.Optimisations import CombineSelectAndCross

# CombineSelectAndCross(ra_tree)

# pp.pprint(ra_tree.projected.to_dict())
