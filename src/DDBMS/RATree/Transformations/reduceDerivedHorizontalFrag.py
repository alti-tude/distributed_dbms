from typing import Union
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Symbols import PredicateOps
from DDBMS.Parser.SQLQuery import checkNonExclusivePredicate
from DDBMS.RATree.Nodes import CrossNode, DerivedHorizontalFragNode, HorizontalFragNode, JoinNode, ProjectNode, RelationNode, SelectNode, Node, UnionNode


def __checkFrag(frag : DerivedHorizontalFragNode) -> bool:
    node = frag
    
    while isinstance(node.parent, (SelectNode, ProjectNode)):
        node = node.parent

    if isinstance(node.parent, JoinNode):
        parent = node.parent

        idx = parent.getChildId(node)
        other_idx = 1-idx
        sibbling = parent.children[other_idx]

        while isinstance(sibbling, (SelectNode, ProjectNode)):
            sibbling = sibbling.children[0]

        if isinstance(sibbling, HorizontalFragNode) and parent.join_predicate == frag.join_predicate:
            if frag.right_frag_name != sibbling.name:
                return False

    return True


def __deleteInvalidBranches(node : Node) -> bool:
    """[summary]

    Args:
        node (Node): [description]

    Returns:
        bool: [return True if delete branch]
    """
    
    if isinstance(node, DerivedHorizontalFragNode):
        return not __checkFrag(node)

    to_delete = []
    delete = False
    for child in node.children:
        if __deleteInvalidBranches(child): 
            to_delete.append(child)
            delete = True

    for child in to_delete:
        node.deleteChild(child)
    
    #return false if not deletable
    if not ( isinstance(node, ProjectNode) or isinstance(node, SelectNode) or isinstance(node, CrossNode) or isinstance(node, JoinNode)):
        return False
    
    return delete

def reduceDerivedHorizontalFrag(node : Node) -> Node:
    if __deleteInvalidBranches(node):
        return None

    return node
