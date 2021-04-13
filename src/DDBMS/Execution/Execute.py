
from mo_dots.datas import Data
from DDBMS.DB import DBUtils, db
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

    if isinstance(cur_node, (UnionNode, CrossNode, FinalProjectNode)):
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
            if isinstance(cur_node, FinalProjectNode):
                executeSelect(cur_node, query_id, cur_node.operation_id)
        else:
            other_site = cur_node.site
            for child in cur_node.children:
                if child.site == Site.CUR_SITE:
                    executeSelect(child, query_id, child.operation_id)
                    DataTransfer.send(other_site, query_id, child.operation_id, child.cols)
    
    elif isinstance(cur_node, JoinNode):

        if Site.CUR_SITE in cur_node.child_sites:
            for child in cur_node.children:
                if child.site == Site.CUR_SITE:
                    executeSelect(child, query_id, child.operation_id)

            if cur_node.child_sites[0] == Site.CUR_SITE:
                #send col
                send_col_obj = cur_node.predicate_cols[0]
                send_from_table = DataTransfer.get(query_id, cur_node.children[0].operation_id)
                with db.returnLists():
                    send_col_data = DBUtils.selectQuery([send_col_obj], send_from_table)
                DataTransfer.send(cur_node.child_sites[1], query_id, cur_node.operation_id+"_1", [send_col_obj], send_col_data)

            if cur_node.child_sites[1] == Site.CUR_SITE:
                #recv col
                cur_table = DataTransfer.get(query_id, cur_node.children[1].operation_id)
                recv_col_as_table = DataTransfer.get(query_id, cur_node.operation_id + "_1")
                
                #semijoin
                with db.returnStrings():
                    semijoin_data = DBUtils\
                                .semijoinQuery(cur_table, recv_col_as_table, cur_node.predicate_cols[1], cur_node.predicate_cols[0])
                    print(semijoin_data)
                    
                with db.returnLists():
                    semijoin_data = DBUtils\
                                .semijoinQuery(cur_table, recv_col_as_table, cur_node.predicate_cols[1], cur_node.predicate_cols[0])
                
                #send joined table
                DataTransfer.send(cur_node.child_sites[0], query_id, cur_node.operation_id + "_2", cur_node.children[1].cols, semijoin_data)

            if cur_node.child_sites[0] == Site.CUR_SITE:
                #recv table
                cur_table = DataTransfer.get(query_id, cur_node.children[0].operation_id)
                recvd_table = DataTransfer.get(query_id, cur_node.operation_id + "_2")

                #join
                with db.returnLists():
                    data = DBUtils.join(cur_table, recvd_table, cur_node.predicate_cols[0], cur_node.predicate_cols[1])
                #put table
                DataTransfer.put(query_id, cur_node.operation_id, data, cur_node.cols, decode=False)


    #TODO handle groupby
    new_node = RelationNode(Table(getTempTableName(query_id, cur_node.operation_id)))    
    if cur_node.parent is not None:
        cur_node.parent.replaceChild(cur_node, new_node)
        new_node.site = cur_node.site
        new_node.operation_id = cur_node.operation_id
        new_node.cols = cur_node.cols