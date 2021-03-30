
from Config import DEBUG
from DDBMS.Execution.Local.Cross import executeCross
from DDBMS.Execution.Local.Union import executeUnion
from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.Execution.DataTransfer import getTempTableName
from . import DataTransfer
from DDBMS.Execution.Site import Site
from DDBMS.RATree.Nodes import CrossNode, FinalProjectNode, JoinNode, Node, ProjectNode, RelationNode, SelectNode, UnionNode
from .Local.Select import executeSelect

def isSelectBranch(cur_node : Node):
    if isinstance(cur_node, RelationNode):
        return True
    
    if isinstance(cur_node, CrossNode) or isinstance(cur_node, JoinNode) or isinstance(cur_node, UnionNode):
        return False

    return isSelectBranch(cur_node.children[0])

def execute(cur_node : Node, query_id):
    if isinstance(cur_node, RelationNode):
        return

    list(map(lambda child : execute(child, query_id), cur_node.children))

    if isinstance(cur_node, ProjectNode) or isinstance(cur_node, SelectNode):
        return

    child_tables = [Table(getTempTableName(query_id, child.operation_id)) for child in cur_node.children]
    for i in range(len(child_tables)):
        if isinstance(cur_node.children[i], RelationNode):
            child_tables[i] = cur_node.children[i].table
    
    if isinstance(cur_node, UnionNode) or isinstance(cur_node, CrossNode) or isinstance(cur_node, FinalProjectNode):
        if cur_node.site == Site.CUR_SITE:
            for child in cur_node.children:
                if child.site == Site.CUR_SITE:
                    executeSelect(child, query_id, child.operation_id, child.cols)
                else:
                    DataTransfer.get(query_id, child.operation_id)
            
            if isinstance(cur_node, UnionNode):
                executeUnion(child_tables, cur_node.cols, query_id, cur_node.operation_id)
            if isinstance(cur_node, CrossNode):
                executeCross(child_tables, cur_node.cols, query_id, cur_node.operation_id)
            if isinstance(cur_node, FinalProjectNode):
                executeSelect(cur_node, query_id, cur_node.operation_id)
        else:
            other_site = cur_node.site
            for child in cur_node.children:
                if child.site == Site.CUR_SITE:
                    executeSelect(child, query_id, child.operation_id)
                    DataTransfer.send(other_site, query_id, child.operation_id, child.cols)
    
    #TODO handle groupby
    #TODO handle naming of columns (duplicates in case of joins or cross between 2 tables having same nodes)
    #TODO handle join

    new_node = RelationNode(Table(getTempTableName(query_id, cur_node.operation_id)))    
    if cur_node.parent is not None:
        cur_node.parent.replaceChild(cur_node, new_node)
        new_node.site = cur_node.site
        new_node.operation_id = cur_node.operation_id
        new_node.cols = cur_node.cols