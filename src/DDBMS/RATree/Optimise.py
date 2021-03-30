from DDBMS.RATree.Transformations import *
from .RATreeBuilder import RATreeBuilder

def optimise():
    ra_tree = RATreeBuilder()
    root = pushSelect(ra_tree.projected)
    # root = combineSelectAndCross(root)
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