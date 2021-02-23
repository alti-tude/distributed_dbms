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


from DDBMS.RATree.Transformations.reduceHorizontalFrag import reduceHorizontalFrag
from DDBMS.RATree.Transformations.Localise import materialiseAllTables, materialiseTable
from DDBMS.RATree.Transformations.MoveUnionUp import moveUnionUp
from DDBMS.RATree.Transformations.PushProject import pushProject
from DDBMS.RATree.Transformations.PushSelect import pushSelect
from DDBMS.Parser.SQLParser import *
from DDBMS.RATree import RATreeBuilder
from pprint import PrettyPrinter 

pp = PrettyPrinter(indent=2, compact=True)

query = "select max(ScreenID) from Screen group by ScreenID;"
parser = SQLParser()
sql_query = parser.parse(query)

ra_tree = RATreeBuilder()
# ra_tree.projected.to_dict()
pp.pprint(materialiseAllTables(ra_tree.projected).to_dict())
# moveUnionUp(ra_tree.projected).to_dict()
# pp.pprint(reduceHorizontalFrag(ra_tree.projected).to_dict())
# from DDBMS.RATree.Optimisations import CombineSelectAndCross

# CombineSelectAndCross(ra_tree)

# pp.pprint(ra_tree.projected.to_dict())
