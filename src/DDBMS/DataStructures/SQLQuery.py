from DDBMS.DataStructures.Table import Table
from typing import Dict, List
from DDBMS.Parser import parseSql
from .Predicate import Predicate, getPredicateObj
from .Symbols import Keywords, PredicateOps

class SQLQuery:
    def __init__(self, *, query_string: str) -> None:
        self.parsed_query = parseSql(query_string)
        
        self.select = None
        self.from_clause = []
        self.where = None
        self.groupby = None
        self.having = None

        if Keywords.SELECT in self.parsed_query:
            self.select = self.parsed_query[Keywords.SELECT]

        if Keywords.FROM in self.parsed_query:
            self.from_clause = self.parsed_query[Keywords.FROM]
        
        if Keywords.WHERE in self.parsed_query:
            self.where = getPredicateObj(self.parsed_query[Keywords.WHERE])
        
        if Keywords.GROUPBY in self.parsed_query:
            self.groupby = self.parsed_query[Keywords.GROUPBY]

        if Keywords.HAVING in self.parsed_query:
            self.having = getPredicateObj(self.parsed_query[Keywords.HAVING])

    def getTables(self) -> List[Table]:
        return self.from_clause

    def filterWherePredicates(self, filter_fn = lambda x: True) -> List[Predicate]:
        if self.where is None:
            return []

        predicate_list = []
        if PredicateOps.AND == self.where.op:
            predicate_list = self.where.operands
        else:
            predicate_list = [self.where]
        
        #list of (index, predicate) tuples
        filtered_list = []
        for i, predicate in enumerate(predicate_list):
            if filter_fn(predicate):
                filtered_list.append((i, predicate))

        return filtered_list
