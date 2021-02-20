
from DDBMS.Parser.SQLQuery.Symbols import Aggregation, PredicateOps
from DDBMS.Parser.SQLQuery.Predicate import Predicate
from DDBMS.Parser.SQLQuery.SQLQuery import SQLQuery
from .Nodes import *
from copy import deepcopy

class RATreeBuilder:
    def __init__(self, sql_query: SQLQuery):
        self.sql_query = sql_query
        
        #bottom up tree

        self.leaves = self.buildTablesAsLeaves()
        self.joined = self.crossTables()
        self.selected = self.seperateSelect(self.sql_query.where, self.joined)
        self.project_before_groupby = self.addProjectBeforeGroupby(self.selected)

        self.gamma_added = self.addGroupby(self.project_before_groupby)
        self.having_added = self.seperateSelect(self.sql_query.having, self.gamma_added)
        self.projected = self.addProject(self.having_added)

    def __repr__(self):
        return str(self.projected)

    def buildTablesAsLeaves(self) -> List[RelationNode]:
        return [RelationNode(table) for table in self.sql_query.tables]

    def crossTables(self):
        cur_node = self.leaves[0]
        for i in range(1, len(self.leaves)):
            cur_node = CrossNode(children=[cur_node, self.leaves[i]])
        
        return cur_node

    def seperateSelect(self, predicates, cur_root):
        cur_node = cur_root

        for predicate in predicates:
            cur_node = SelectNode(predicate=predicate, children=[cur_node])
        
        return cur_node
    
    def addProjectBeforeGroupby(self, cur_root):
        required_columns = []
        for predicate in self.sql_query.having:
            required_columns.extend(predicate.getAllColumns())
        
        required_columns.extend(self.sql_query.groupby)
        required_columns.extend(self.sql_query.select)

        return ProjectNode(columns=required_columns, children=[cur_root])

    def addGroupby(self, cur_root):
        cur_node = cur_root

        group_by_cols = self.sql_query.groupby

        if len(group_by_cols) > 0:
            return GroupbyNode(group_by_columns=group_by_cols, children=[cur_node])
        return cur_node

    def addProject(self, cur_root):
        cur_node = cur_root

        project_cols = self.sql_query.select

        return ProjectNode(columns=project_cols, children=[cur_node])