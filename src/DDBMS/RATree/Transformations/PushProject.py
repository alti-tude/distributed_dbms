from DDBMS.Parser.SQLQuery.Symbols import Aggregation
from DDBMS.RATree.RATreeBuilder import RATreeBuilder
from DDBMS.RATree.Nodes import *

def optimizeProject(ra_tree : RATreeBuilder, node):
    if isinstance(node, RelationNode):
        return ra_tree.sql_query.filterCols(table=node.table, aggregation=Aggregation.NONE)

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

            if new_project_cols == cols:
                delete_cur_node = True
            
            for i, grandchild in enumerate(child.children):
                new_node = ProjectNode(columns=new_project_cols, children=[grandchild])
                child.replaceChildById(i, new_node)

        elif isinstance(child, ProjectNode):
            delete_cur_node = True
            child.columns = list(set(cols + child.columns))
        
        elif isinstance(child, UnionNode) or isinstance(child, CrossNode):
            delete_cur_node = True
            for i, grandchild in enumerate(child.children):
                new_node = ProjectNode(columns=cols, children=[grandchild])
                child.replaceChildById(i, new_node)

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