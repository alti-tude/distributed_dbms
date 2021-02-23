from DDBMS.RATree.Nodes import CrossNode, HorizontalFragNode, JoinNode, ProjectNode, RelationNode, SelectNode, Node, UnionNode, VerticalFragNode


def __checkFrag(frag : VerticalFragNode) -> bool:
    node = frag
    while node is not None and \
        ( isinstance(node, ProjectNode) or isinstance(node, VerticalFragNode)):

        if isinstance(node, ProjectNode):
            #FIXME DONT PUSH DOWN SELECT FOR VERTICAL FRAG

            #assuming no select pushdown 
            #project will have join or another project as direct ancestor
            #hence no point of projecting a column
            if len(set(node.columns).intersection(set(frag.columns))) <= 1: 
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
    
    if isinstance(node, VerticalFragNode):
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
    if isinstance(node, JoinNode) and delete:
        node.parent.replaceChild(node, node.children[0])

    if not ( isinstance(node, ProjectNode)):
        return False
    
    return delete

def reduceVerticalFrag(node : Node) -> Node:
    if __deleteInvalidBranches(node):
        return None

    return node
