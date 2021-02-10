from DDBMS.DataStructures.Symbols import Aggregation, PredicateOps
from DDBMS.DataStructures.Predicate import Predicate
from DDBMS.DataStructures.SQLQuery import SQLQuery
from .Nodes import *
from copy import deepcopy

class RATreeBuilder:
    def __init__(self, sql_query: SQLQuery):
        self.sql_query = deepcopy(sql_query)
        
        self.where_pred_alive = [True for i in self.sql_query.filterWherePredicates()]

        self.leaves = self.buildTablesAsLeaves()
        self.joined = self.joinLeaves()

        live_preds = []
        for (idx, pred) in self.sql_query.filterWherePredicates():
            if self.where_pred_alive[idx]: live_preds.append(pred)
        self.selected = self.seperateSelect(live_preds, self.joined)

        self.gamma_added = self.addGroupby(self.selected)

        live_preds = [predicate for (idx,predicate) in self.sql_query.filterHavingPredicates()]
        self.having_added = self.seperateSelect(live_preds, self.gamma_added)
        
        self.projected = self.addProject(self.having_added)

    def buildTablesAsLeaves(self) -> List[Table]:
        return [table for table in self.sql_query.getTables()]

    def joinLeaves(self):
        def filterEqPred(predicate : Predicate) -> bool:
            return (
                predicate.op == PredicateOps.EQ and
                len(predicate.operands) == 2 and
                isinstance(predicate.operands[0], Column) and
                isinstance(predicate.operands[1], Column) and
                predicate.operands[0].table.alias != predicate.operands[1].table.alias
            )

        adj_list = [[] for i in self.leaves]

        def indexOfTable(table):
            for i, leaf in enumerate(self.leaves):
                if leaf.alias == table.alias:
                    return i

        for (idx, predicate) in self.sql_query.filterWherePredicates(filter_fn=filterEqPred):
            lhs_table = predicate.operands[0].table
            rhs_table = predicate.operands[1].table

            lhs_index = indexOfTable(lhs_table)
            rhs_index = indexOfTable(rhs_table)

            adj_list[lhs_index].append((rhs_index, predicate, idx))
            adj_list[rhs_index].append((lhs_index, predicate, idx))

        visited = [False for i in self.leaves]

        def dfs(u, visited, adj_list):
            visited[u] = True
            cur_join = RelationNode(table=self.leaves[u])

            for (v, predicate, idx) in adj_list[u]:
                if not visited[v]:
                    return_value = dfs(v, visited, adj_list)
                    cur_join = JoinNode(
                        join_predicate=predicate, 
                        children=[cur_join, return_value]
                    )
                    self.where_pred_alive[idx] = False

            return cur_join

        to_cross = []
        for i in range(len(self.leaves)):
            if not visited[i]:
                to_cross.append(dfs(i, visited, adj_list))
        
        if len(to_cross) == 1:
            return to_cross[0]
        else:
            return CrossNode(children=to_cross)

    def seperateSelect(self, live_preds, cur_root):
        cur_node = cur_root

        for predicate in live_preds:
            cur_node = SelectNode(predicate=predicate, children=[cur_node])
        
        return cur_node
    
    def addGroupby(self, cur_root):
        cur_node = cur_root

        group_by_cols = self.sql_query.getGroupByCols()
        aggregations = [col for col in self.sql_query.getAllCols() if col.aggregation != Aggregation.NONE]
        
        if len(group_by_cols) > 0:
            return GroupbyNode(group_by_columns=group_by_cols, aggregations=aggregations, children=[cur_node])
        return cur_node

    def addProject(self, cur_root):
        cur_node = cur_root

        project_cols = self.sql_query.getSelectCols()

        return ProjectNode(columns=project_cols, children=[cur_node])