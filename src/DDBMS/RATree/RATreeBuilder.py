
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

        live_preds = []
        for (idx, pred) in self.sql_query.filterWherePredicates():
            if self.where_pred_alive[idx]: live_preds.append(pred)
        self.selected = self.seperateSelect(live_preds, self.joined)

        self.gamma_added = self.addGroupby(self.selected)

        live_preds = [predicate for (idx,predicate) in self.sql_query.filterHavingPredicates()]
        self.having_added = self.seperateSelect(live_preds, self.gamma_added)
        
        self.projected = self.addProject(self.having_added)

    def buildTablesAsLeaves(self) -> List[RelationNode]:
        return [RelationNode(table) for table in self.sql_query.tables]

    #TODO
    def joinLeaves(self):
        self.sql_query.buildJoin()
        
        visited = [False for i in self.leaves]
        cur_node = self.leaves[self.leaves.index(cur_table)]
        visited[self.leaves.index(cur_table)] = True

        while True:
            cur_predicate == None
            for predicate in self.join:
                if predicate.operands[0].table == cur_table:
                    cur_predicate = predicate
                    break
            
            if cur_predicate is None:
                break

            next_table = cur_predicate.operands[1].table
            next_node = self.leaves[self.leaves.index(next_table)]

            cur_node = JoinNode(self.sql_query.join[i], children=[cur_node, next_node])
            cur_table = next_table
            visited[self.leaves.index(cur_table)] = True

        return cur_node

        to_cross = []
        for i in range(len(self.leaves)):
            if not visited[i]:
                to_cross.append(join())
        
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