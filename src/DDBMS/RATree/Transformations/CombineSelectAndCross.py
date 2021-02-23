from DDBMS.RATree.Nodes import CrossNode, JoinNode, Node, SelectNode
from DDBMS.RATree.RATreeBuilder import RATreeBuilder


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

def CombineSelectAndCross(root):
    __recursiveCombine(root)
    return root