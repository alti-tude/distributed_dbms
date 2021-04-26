
from typing import Union

from moz_sql_parser import sql_parser
from DDBMS.Parser.SQLQuery.Symbols import Aggregation, PredicateOps
from DDBMS.Parser.SQLQuery.Predicate import Predicate
from DDBMS.Parser.SQLQuery.SQLQuery import SQLQuery
from .Nodes import *
from copy import deepcopy

#region BUILDER FUNCTIONS
def seperateSelect(predicates : Union[List[Predicate], Predicate], cur_root) -> Node:
    """seperate selects into multiple selects

    Args:
        predicates (Union[List[Predicate], Predicate]): works for both list and predicate
        cur_root ([type]): [description]

    Returns:
        Node: [description]
    """

    if isinstance(predicates, Predicate):
        if predicates.operator == PredicateOps.AND:
            predicates = predicates.operands
        else:
            predicates = [predicates]

    cur_node = cur_root

    for predicate in predicates:
        cur_node = SelectNode(predicate=predicate, children=[cur_node])
    
    return cur_node

def crossNodes(nodes):
    cur_node = nodes[0]
    for i in range(1, len(nodes)):
        cur_node = CrossNode(children=[cur_node, nodes[i]])
    
    return cur_node

def addProjectWithoutAgg(sql_query : SQLQuery, cur_root : Node):
    required_columns = []
    if isinstance(sql_query.having, Predicate):
        required_columns.extend(sql_query.having.getAllColumns())
    required_columns.extend(sql_query.groupby)
    required_columns.extend(sql_query.select)

    for i, col in enumerate(required_columns):
        if col.aggregation != Aggregation.NONE:
            required_columns[i] = sql_query.newColumn(col.name, col.table, col.alias, Aggregation.NONE)
    
    required_columns = list(set(required_columns))
    return ProjectNode(columns=required_columns, children=[cur_root])

def addGroupby(group_by_cols, having_predicate : Predicate, cur_root):
    cur_node = cur_root

    if len(group_by_cols) > 0:
        return GroupbyNode(group_by_cols, having_predicate, children=[cur_node])

    return cur_node

#endregion

class RATreeBuilder:
    #TODO store this in a store object
    def __init__(self):
        self.sql_query = SQLQuery.get()

        #bottom up tree
        self.leaves = [RelationNode(table) for table in self.sql_query.tables]
        self.joined = crossNodes(self.leaves)
        self.selected = seperateSelect(self.sql_query.where, self.joined)
        self.project_before_groupby = addProjectWithoutAgg(self.sql_query, self.selected)

        self.gamma_added = addGroupby(self.sql_query.groupby, self.sql_query.having, self.project_before_groupby)
        self.projected = FinalProjectNode(columns=self.sql_query.select, children=[self.gamma_added])

    def __repr__(self):
        return str(self.projected)
