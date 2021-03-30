from DDBMS.Parser.SQLQuery.Symbols import PredicateOps
from DDBMS.RATree.Nodes import CrossNode, JoinNode, Node, RelationNode, SelectNode

def __getSelectNodes(node):
    if isinstance(node, RelationNode):
        return []

    select_nodes = []
    if isinstance(node, SelectNode) \
    and len(node.predicate.getAllColumns()) == 2 \
    and node.predicate.operator == PredicateOps.EQ:
        select_nodes.append(node)
    
    for child in node.children:
        select_nodes += __getSelectNodes(child)

    return select_nodes
    
def __pushSelect(cur_node: SelectNode):
    while isinstance(cur_node.children[0], SelectNode):
        parent = cur_node.parent
        child = cur_node.children[0]

        parent.replaceChild(cur_node, child)
        grand_child = child.replaceChildById(0, cur_node)
        cur_node.replaceChild(child, grand_child)

def __recursiveCombine(cur_node : Node):
    if len(cur_node.children) == 0: return

    for child in cur_node.children:
        __recursiveCombine(child)

    if isinstance(cur_node, SelectNode):
        parent : Node = cur_node.parent
        child : Node = cur_node.children[0]
        
        if isinstance(child, CrossNode):
            new_node = JoinNode(cur_node.predicate, children=child.children)
            parent.replaceChild(cur_node, new_node)

def combineSelectAndCross(root):
    select_nodes = __getSelectNodes(root)
    
    for select_node in select_nodes: 
        __pushSelect(select_node)

    __recursiveCombine(root)
    return root