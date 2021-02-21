from typing import List, Tuple
from copy import deepcopy
from DDBMS.RATree.Nodes import CrossNode, JoinNode, Node, ProjectNode, SelectNode, UnionNode


def __getAllUnions(cur_node : Node) -> List[UnionNode]:
    result = []
    
    if isinstance(cur_node, UnionNode):
        result.append(cur_node)

    for child in cur_node.children:
        result.extend(__getAllUnions(child))
    
    return result

def __pullUp(union : UnionNode) -> Tuple[bool, Node]:
    parent : Node = union.parent
    grand_parent : Node = None if parent is None else parent.parent

    new_nodes = []
    if isinstance(parent, SelectNode):
        for child in union.children:
            new_nodes.append(SelectNode(predicate = parent.predicate, children=[child]))
    
    elif isinstance(parent, ProjectNode):
        for child in union.children:
            new_nodes.append(ProjectNode(columns=parent.columns, children=[child]))
    
    elif isinstance(parent, CrossNode):
        for child in union.children:
            union_idx = parent.getChildId(union)
            new_node = CrossNode(children=deepcopy(parent.children))
            new_node.replaceChildById(union_idx, child)
            new_nodes.append(new_node)

    elif isinstance(parent, JoinNode):
        for child in union.children:
            union_idx = parent.getChildId(union)
            new_node = JoinNode(join_predicate=parent.join_predicate, children=deepcopy(parent.children))
            new_node.replaceChildById(union_idx, child)
            new_nodes.append(new_node)

    elif isinstance(parent, UnionNode):
        for child in union.children:
            parent.addChild(child)
        parent.deleteChild(union)
        return True, None
        
    else: return False, None

    for (child, new_node) in list(zip(union.children, new_nodes)):
        union.replaceChild(child, new_node)

    if grand_parent is None:
        union.makeRoot()
        return True, union
    else:
        grand_parent.replaceChild(parent, union)
        return True, None
    
def __moveUnionUpStep(root : Node) -> Tuple[bool, Node]:
    unions = __getAllUnions(root)

    is_pulled = False
    for union in unions:
        pulled, new_root = __pullUp(union)
        if new_root is not None:
            root = new_root
        
        is_pulled = is_pulled or pulled
    
    return is_pulled, root

def moveUnionUp(root : Node) -> Node:
    is_pulled, root = __moveUnionUpStep(root)

    while is_pulled:
        is_pulled, root = __moveUnionUpStep(root)
    
    return root