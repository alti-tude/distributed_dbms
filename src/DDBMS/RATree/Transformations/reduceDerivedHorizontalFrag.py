from typing import Union
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Symbols import PredicateOps
from DDBMS.Parser.SQLQuery import checkNonExclusivePredicate
from DDBMS.RATree.Nodes import CrossNode, DerivedHorizontalFragNode, HorizontalFragNode, JoinNode, ProjectNode, RelationNode, SelectNode, Node, UnionNode


def __checkFrag(frag : DerivedHorizontalFragNode) -> bool:
    node = frag
    
    if isinstance(node.parent, JoinNode):
        idx = node.parent.getChildId(node)
        other_idx = 1-idx
        sibbling = node.parent[other_idx]
        if isinstance(sibbling, HorizontalFragNode) and node.parent.join_predicate == node.join_predicate:
            if node.right_frag_name != sibbling.name:
                return False

    return True


def __deleteInvalidBranches(node : Node) -> bool:
    """[summary]

    Args:
        node (Node): [description]

    Returns:
        bool: [return True if delete branch]
    """
    
    if isinstance(node, JoinNode):
        if isinstance(node.children[0], DerivedHorizontalFragNode):
            return not __checkFrag(node.children[0])
        if isinstance(node.children[1], DerivedHorizontalFragNode):
            return not __checkFrag(node.children[1])
    
    to_delete = []
    delete = False
    for child in node.children:
        if __deleteInvalidBranches(child): 
            to_delete.append(child)
            delete = True

    for child in to_delete:
        node.deleteChild(child)
    
    #return false if not deletable
    if not ( isinstance(node, ProjectNode) or isinstance(node, SelectNode) ):
        return False
    
    return delete

def reduceDerivedHorizontalFrag(node : Node) -> Node:
    if __deleteInvalidBranches(node):
        return None

    return node
