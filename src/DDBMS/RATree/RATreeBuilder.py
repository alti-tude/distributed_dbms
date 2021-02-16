
from DDBMS.Parser.SQLQuery.Symbols import Aggregation, PredicateOps
from DDBMS.Parser.SQLQuery.Predicate import Predicate
from DDBMS.Parser.SQLQuery.SQLQuery import SQLQuery
from .Nodes import *
from copy import deepcopy

class RATreeBuilder:
    def __init__(self, sql_query: SQLQuery):
        self.sql_query = deepcopy(sql_query)
        
        self.where_pred_alive = [True for i in self.sql_query.filterWherePredicates()]

        self.leaves = self.buildTablesAsLeaves()
        self.joined = self.joinLeaves()
        self.selected = self.seperateSelect(self.sql_query.where, self.joined)
        self.gamma_added = self.addGroupby(self.selected)
        self.having_added = self.seperateSelect(self.sql_query.having, self.gamma_added)
        self.projected = self.addProject(self.having_added)

    def buildTablesAsLeaves(self) -> List[RelationNode]:
        return [RelationNode(table) for table in self.sql_query.tables]

    def joinLeaves(self):
        self.sql_query.buildJoin()
        
        cur_table = self.sql_query.join[0].operands[0].table
        cur_node = self.leaves[self.leaves.index(cur_table)]

        joined_table_mask = [False for i in self.leaves]
        joined_table_mask[self.leaves.index(cur_table)] = True
        to_cross = []

        for predicate in self.sql_query.join:
            if predicate.operands[0].table == cur_table:
                cur_table = predicate.operands[1].table
                next_node = self.leaves[self.leaves.index(cur_table)]
                cur_node = JoinNode(predicate, children=[cur_node, next_node])
            else:
                to_cross.append(cur_node)
                cur_table = predicate.operands[0].table
                cur_node = self.leaves[self.leaves.index(cur_table)]
    
            joined_table_mask[self.leaves.index(cur_table)] = True

        to_cross.append(cur_node)

        for i in range(len(self.leaves)):
            if not joined_table_mask[i]:
                to_cross.append(self.leaves[i])
        
        if len(to_cross) == 1:
            return to_cross[0]
        else:
            return CrossNode(children=to_cross)

    def seperateSelect(self, predicates, cur_root):
        cur_node = cur_root

        for predicate in predicates:
            cur_node = SelectNode(predicate=predicate, children=[cur_node])
        
        return cur_node
    
    def addGroupby(self, cur_root):
        cur_node = cur_root

        group_by_cols = self.sql_query.groupby()

        if len(group_by_cols) > 0:
            return GroupbyNode(group_by_columns=group_by_cols, children=[cur_node])
        return cur_node

    def addProject(self, cur_root):
        cur_node = cur_root

        project_cols = self.sql_query.select

        return ProjectNode(columns=project_cols, children=[cur_node])