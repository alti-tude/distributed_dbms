from DDBMS.RATree.RATreeBuilder import crossNodes
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Symbols import PredicateOps
from DDBMS.Parser.SQLQuery import checkNonExclusivePredicate
from DDBMS.RATree.Nodes import CrossNode, HorizontalFragNode, JoinNode, ProjectNode, RelationNode, SelectNode, Node, UnionNode


def __checkFrag(frag : HorizontalFragNode) -> bool:
    node = frag
    while node is not None and \
        ( isinstance(node, ProjectNode) or isinstance(node, SelectNode) or isinstance(node, HorizontalFragNode)):

        if isinstance(node, SelectNode):
            if not checkNonExclusivePredicate(node.predicate, frag.predicate):
                return False
        
        node = node.parent

    return True


def __deleteInvalidBranches(node : Node) -> bool:
    """[summary]

    Args:
        node (Node): [description]

    Returns:
        bool: [return True if delete branch]
    """
    
    if isinstance(node, HorizontalFragNode):
        return not __checkFrag(node)
    
    if isinstance(node, RelationNode):
        return False

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

def reduceHorizontalFrag(node : Node) -> Node:
    if __deleteInvalidBranches(node):
        return None

    return node
