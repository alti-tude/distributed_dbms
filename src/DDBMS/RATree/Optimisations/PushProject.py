import copy
from DDBMS.RATree.Nodes import *

def insertNodeBetween(parent, child_idx, insert_node):
    new_child = parent.replaceChildById(child_idx, insert_node)
    insert_node.replaceChildById(0, new_child)


def optimizeProject(ra_tree, node):
    if isinstance(node, RelationNode):
        return ra_tree.sql_query.filterCols(node.table)

    node_children = node.children
    delete_cur_node = False

    if isinstance(node, ProjectNode):
        cols = node.columns
        child = node_children[0]

        if isinstance(child, SelectNode) or isinstance(child, JoinNode):
            child_cols = []
            if isinstance(child, SelectNode):
                child_cols = child.predicate.getAllColumns()
            else:
                child_cols = child.join_predicate.getAllColumns()
            new_project_cols = list(set(cols + child_cols))

            new_node = node
            if new_project_cols == cols:
                delete_cur_node = True
            
            for i in range(len(children)):
                if new_project_cols != cols:
                    new_node = copy.deepcopy(node)
                    new_node.columns = new_project_cols
                insertNodeBetween(child, i, new_node)

        elif isinstance(child, ProjectNode):
            delete_cur_node = True
            child.columns = list(set(cols + child.columns))
        
        elif isinstance(child, UnionNode) or isinstance(child, CrossNode):
            delete_cur_node = True
            for i in range in len(child.children):
                new_node = copy.deepcopy(node)
                insertNodeBetween(child, i, new_node)

    subtree_cols = []
    for child in node_children:
        subtree_cols += optimizeProject(ra_tree, child)
    
    if not delete_cur_node and isinstance(node, ProjectNode):
        subtree_cols = list(set(node.columns).intersection(subtree_cols))
        node.columns = subtree_cols

    if delete_cur_node or (isinstance(node, ProjectNode) and len(subtree_cols) == 0):
        node.parent.replaceChild(node, node.children[0])

    return subtree_cols


def pushProject(ra_tree):
    main_project_node = ra_tree.project_before_groupby
    optimizeProject(ra_tree, main_project_node)
    return ra_tree