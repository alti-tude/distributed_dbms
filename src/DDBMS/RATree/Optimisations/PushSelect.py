from DDBMS.RATree.Nodes import *

def getSelectNodes(node):
    select_nodes = []
    if isinstance(node, SelectNode):
        select_nodes.append(node)
    
    for child in node.children:
        select_nodes += getSelectNodes(child)

    return select_nodes


def getNewParent(select_cols, node):
    if isinstance(node, RelationNode):
        for select_col in select_cols:
            if select_col.table == node.table:
                return True       
        return None
    
    push_select_down = True
    deeper_new_parent = None
    insert_child_idx = -1

    for idx, child in enumerate(node.children):
        possible_deeper_new_parent = getNewParent(select_cols, child)
        if possible_deeper_new_parent is not None:
            if insert_child_idx != -1:
                push_select_down = False
                break
            deeper_new_parent = possible_deeper_new_parent
            insert_child_idx = idx
    
    if push_select_down and deeper_new_parent != None:
        if deeper_new_parent != True:
            return deeper_new_parent
        elif isinstance(node, JoinNode) or isinstance(node, CrossNode):
            return [node, insert_child_idx]
        else:
            return [node, -1]

    if isinstance(node, ProjectNode) or \
       isinstance(node, GroupbyNode) or \
       isinstance(node, UnionNode):
       return [node, -1]
    
    return None
    

def insertSelect(parent, child_idx, select_node):
    select_node.parent.replaceChild(select_node, select_node.children[0])
    old_child = parent.replaceChildById(select_node, child_idx)
    select_node.replaceChildById(old_child, 0)


def pushSelect(ra_tree):
    select_nodes = getSelectNodes(ra_tree.projected)
    if len(select_nodes) == 0:
        return ra_tree

    for select_node in select_nodes:
        select_node_cols = select_node.predicate.getAllColumns()
        parent_detail = getNewParent(select_node_cols, select_node)

        if parent_detail is not None:
            parent, child_idx = parent_detail
            if child_idx != -1:
                insertSelect(parent, child_idx, select_node)
            else:
                for i in range(len(parent.children)):
                    insertSelect(parent, i, select_node)
    
    return ra_tree
