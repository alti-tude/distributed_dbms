
from DDBMS.DB import DBUtils, db
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

    if isinstance(cur_node, (UnionNode, CrossNode, JoinNode, FinalProjectNode)):
        if cur_node.site == Site.CUR_SITE:
            for child in cur_node.children:
                if child.site == Site.CUR_SITE:
                    executeSelect(child, query_id, child.operation_id)
                else:
                    DataTransfer.get(query_id, child.operation_id)
            
            if isinstance(cur_node, UnionNode):
                executeUnion(cur_node, query_id, cur_node.operation_id)
            if isinstance(cur_node, CrossNode):
                executeCross(cur_node, query_id, cur_node.operation_id)
            if isinstance(cur_node, JoinNode):
                if cur_node.normal_join:
                    tables = [
                        DataTransfer.get(query_id, cur_node.children[0].operation_id), 
                        DataTransfer.get(query_id, cur_node.children[1].operation_id)
                    ]
                    t1 = tables[0]
                    t2 = tables[1]
                    with db.returnLists():
                        data = DBUtils.join(t1, t2, *cur_node.join_cols)
                    DataTransfer.put(query_id, cur_node.operation_id, data, cur_node.cols, decode=False)
                else:
                    other_child_idx = cur_node.semijoin_transfer_child
                    current_table = DataTransfer.get(query_id, cur_node.children[1-other_child_idx].operation_id)

                    print(cur_node.semijoin_transfer_col.temp_name)
                    with db.returnStrings():
                        col_to_send = DBUtils.selectQuery([cur_node.semijoin_transfer_col], current_table)
                        print(col_to_send)
                    with db.returnLists():
                        col_to_send = DBUtils.selectQuery([cur_node.semijoin_transfer_col], current_table)

                    print(col_to_send)
                    other_site = cur_node.children[other_child_idx].site
                    DataTransfer.send(other_site, query_id, cur_node.operation_id + "_1", [cur_node.semijoin_transfer_col], col_to_send)

                    other_table = DataTransfer.get(query_id, cur_node.operation_id + "_2")

                    with db.returnLists():
                        data = DBUtils.join(current_table, other_table, cur_node.join_cols[1-other_child_idx], cur_node.join_cols[other_child_idx])
                    
                    DataTransfer.put(query_id, cur_node.operation_id, data, cur_node.cols, decode=False)

            if isinstance(cur_node, FinalProjectNode):
                executeSelect(cur_node, query_id, cur_node.operation_id)
        else:
            other_site = cur_node.site
            for child in cur_node.children:
                if child.site == Site.CUR_SITE:
                    executeSelect(child, query_id, child.operation_id)
                    DataTransfer.send(other_site, query_id, child.operation_id, child.cols)

            if isinstance(cur_node, JoinNode) and not cur_node.normal_join and cur_node.children[cur_node.semijoin_transfer_child].site == Site.CUR_SITE:
                other_child_idx = 1-cur_node.semijoin_transfer_child
                other_site = cur_node.children[other_child_idx].site
                other_col_as_table = DataTransfer.get(query_id, cur_node.operation_id + "_1")
                
                current_table = DataTransfer.get(query_id, cur_node.children[1-other_child_idx].operation_id)
                current_cols = cur_node.children[1-other_child_idx].cols
                with db.returnLists():
                    semijoined_data = DBUtils.semijoinQuery(current_table, other_col_as_table, cur_node.join_cols[1-other_child_idx], cur_node.join_cols[other_child_idx])
                DataTransfer.send(other_site, query_id, cur_node.operation_id + "_2", current_cols, semijoined_data)

    #TODO handle groupby
    #TODO handle naming of columns (duplicates in case of joins or cross between 2 tables having same nodes)
    #TODO handle join

    new_node = RelationNode(Table(getTempTableName(query_id, cur_node.operation_id)))    
    if cur_node.parent is not None:
        cur_node.parent.replaceChild(cur_node, new_node)
        new_node.site = cur_node.site
        new_node.operation_id = cur_node.operation_id
        new_node.cols = cur_node.cols