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

<<<<<<< HEAD
query = "select * from Theater where Location!='Hyderabad' group by TheaterID;"
=======
query = "select * from Movie;"
>>>>>>> bbd2ba5d68f68fbb5b0c83b2a58daab67a0f6d35
parser = SQLParser()
sql_query = parser.parse(query)

ra_tree = RATreeBuilder()
<<<<<<< HEAD
ra_tree.projected.to_dict()
materialiseAllTables(ra_tree.projected).to_dict()
moveUnionUp(ra_tree.projected).to_dict()
pp.pprint(reduceHorizontalFrag(ra_tree.projected).to_dict())
=======
pp.pprint(ra_tree.projected.to_dict())
# ra_tree = pushSelect(ra_tree)
# pp.pprint(ra_tree.projected.to_dict())
# ra_tree = pushProject(ra_tree)
# pp.pprint(ra_tree.projected.to_dict())

pp.pprint(materialiseAllTables(ra_tree.projected).to_dict())
# pp.pprint(moveUnionUp(ra_tree.projected).to_dict())

>>>>>>> bbd2ba5d68f68fbb5b0c83b2a58daab67a0f6d35
# from DDBMS.RATree.Optimisations import CombineSelectAndCross

# CombineSelectAndCross(ra_tree)

# pp.pprint(ra_tree.projected.to_dict())
