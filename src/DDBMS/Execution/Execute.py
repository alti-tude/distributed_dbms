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

def execute(sql_query : str):
    SQLQuery.reset()
    root = getRATree(sql_query)

def getRATree(query : str):
    parser = SQLParser()
    try:
        parser.parse(query)

        ra_tree = RATreeBuilder()
        root = ra_tree.projected
        root = pushSelect(ra_tree.projected)
        root = CombineSelectAndCross(root)
        root = pushProject(root)

        #? Materialise handles reduce vertical
        
        root = materialiseAllTables(root)
        root = pushSelect(root)
        root = pushProject(root)
        root = moveUnionUp(root)
        root = reduceHorizontalFrag(root)

        root = pushSelect(root)
        root = pushProject(root)
        root = reduceDerivedHorizontalFrag(root)

        root = pushSelect(root)
        root = pushProject(root)

        return root
    except Exception as e:
        if Config.DEBUG:
            traceback.print_exc()
        print("An exception has occured. Please verify the query.")


    