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


from DDBMS.RATree.Transformations.CombineSelectAndCross import CombineSelectAndCross
from DDBMS.RATree.Transformations.reduceHorizontalFrag import reduceHorizontalFrag
from DDBMS.RATree.Transformations.reduceDerivedHorizontalFrag import reduceDerivedHorizontalFrag
from DDBMS.RATree.Transformations.Localise import materialiseAllTables, materialiseTable
from DDBMS.RATree.Transformations.MoveUnionUp import moveUnionUp, __moveUnionUpStep
from DDBMS.RATree.Transformations.PushProject import pushProject
from DDBMS.RATree.Transformations.PushSelect import pushSelect
from DDBMS.Parser.SQLParser import *
from DDBMS.RATree import RATreeBuilder
from pprint import PrettyPrinter 
import Config
from treelib import Tree
import traceback

pp = PrettyPrinter(indent=2, compact=True)

query = "select ScreenID from Screen, Theater where Screen.TheaterID = Theater.TheaterID and Theater.Location = 'Delhi';"
parser = SQLParser()
sql_query = parser.parse(query)

ra_tree = RATreeBuilder()
root = pushSelect(ra_tree.projected)
print("="*20)
root = CombineSelectAndCross(root)
root = pushProject(root)
root = materialiseAllTables(root)
root = moveUnionUp(root)
root = pushSelect(root)
root = reduceHorizontalFrag(root)
# root = pushProject(root)
root = reduceDerivedHorizontalFrag(root)
tree = Tree()
root.to_treelib(tree)
tree.show()

SQLQuery.reset()
query = "select count(MovieID) from Movie;"
parser = SQLParser()
sql_query = parser.parse(query)

print("="*20)
ra_tree = RATreeBuilder()
root = pushSelect(ra_tree.projected)
root = CombineSelectAndCross(root)
root = pushProject(root)
tree = Tree()
root.to_treelib(tree)
tree.show()
root = materialiseAllTables(root)
root = pushProject(root)

root = moveUnionUp(root)
root = pushSelect(root)
root = reduceHorizontalFrag(root)
tree = Tree()
root.to_treelib(tree)
tree.show()

root = pushProject(root)
root = reduceDerivedHorizontalFrag(root)
tree = Tree()
root.to_treelib(tree)
tree.show()

while True:
    query = input("> ")

    SQLQuery.reset()
    parser = SQLParser()
    
    try:
        parser.parse(query)

        ra_tree = RATreeBuilder()
        root = pushSelect(ra_tree.projected)
        root = CombineSelectAndCross(root)
        root = pushProject(root)
        root = materialiseAllTables(root)
        
        #TODO show tree
        root = pushSelect(root)
        root = pushProject(root)
        root = moveUnionUp(root)
        root = reduceHorizontalFrag(root)

        root = pushProject(root)
        root = pushSelect(root)
        root = reduceDerivedHorizontalFrag(root)
        #TODO show tree
        tree = Tree()
        root.to_treelib(tree)
        tree.show()
    except Exception as e:
        if Config.DEBUG:
            traceback.print_exc()
        print("An exception has occured. Please verify the query.")

