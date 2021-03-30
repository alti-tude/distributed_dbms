from DDBMS.RATree.Nodes import *
from DDBMS.Parser.SQLQuery.Symbols import Aggregation

def getSelectNodes(node):
    if isinstance(node, RelationNode):
        return []

    select_nodes = []
    if isinstance(node, SelectNode):
        cols = node.predicate.getAllColumns()
        valid_where_clause = True
        for col in cols:
            if col.aggregation != Aggregation.NONE:
                valid_where_clause = False
                break
        if valid_where_clause:
            select_nodes.append(node)
    
    for child in node.children:
        select_nodes += getSelectNodes(child)

    return select_nodes

def getNewParent(select_cols, node):
    if isinstance(node, RelationNode):
        for select_col in select_cols:
            if select_col.table == node.table:
                return [None, -1, True] # [Deeper parent, index bw parent & child, whether select contains columns from subtree]
        return [None, -1, False]
    
    valid_subtrees = []
    for idx, child in enumerate(node.children):
        subtree_details = getNewParent(select_cols, child)
        if subtree_details[2] == True:
            valid_subtrees.append((subtree_details, idx))
    
    if len(valid_subtrees) == 1:
        subtree_details, child_idx = valid_subtrees[0]
        if subtree_details[0] is not None:
            return subtree_details
        else:
            return [node, child_idx, True]
    elif len(valid_subtrees) > 1:
        if isinstance(node, UnionNode):
            return [node, -1, True]
        return [None, -1, True]
    else:
        return [None, -1, False]
    

def insertSelect(parent, child_idx, select_node):
    select_node_copy = select_node.copy()
    old_child = parent.replaceChildById(child_idx, select_node_copy)
    select_node_copy.replaceChildById(0, old_child)


def pushSelect(root):
    select_nodes = getSelectNodes(root)

    for select_node in select_nodes:
        select_node_cols = select_node.predicate.getAllColumns()
        parent_detail = getNewParent(select_node_cols, select_node.children[0])

        if parent_detail[0] is not None:
            parent, child_idx, _ = parent_detail
            select_node.parent.replaceChild(select_node, select_node.children[0])
            if child_idx != -1:
                insertSelect(parent, child_idx, select_node)
            else:
                for i in range(len(parent.children)):
                    insertSelect(parent, i, select_node)
    
    return root
