from DDBMS.DataStructures.Column import Column
import json
from DDBMS.DataStructures.Table import Table
from typing import Dict, List
from DDBMS.Parser import parse_sql
from .Predicate import Predicate, buildPredicateTree
from .Symbols import Keywords, PredicateOps

class SQLQuery:
    def __init__(self, *, query_string: str) -> None:
        self.parsed_query = parse_sql(query_string)
        
        self.select = []
        self.from_clause = []
        self.where = None
        self.groupby = []
        self.having = None

        if Keywords.SELECT in self.parsed_query:
            self.select = self.parsed_query[Keywords.SELECT]

        if Keywords.FROM in self.parsed_query:
            self.from_clause = self.parsed_query[Keywords.FROM]
        
        if Keywords.WHERE in self.parsed_query:
            self.where = buildPredicateTree(self.parsed_query[Keywords.WHERE])
        
        if Keywords.GROUPBY in self.parsed_query:
            self.groupby = self.parsed_query[Keywords.GROUPBY]

        if Keywords.HAVING in self.parsed_query:
            self.having = buildPredicateTree(self.parsed_query[Keywords.HAVING])

    def __repr__(self) -> str:
        output = {
            'Query': {
                'select': json.loads(str(self.select)),
                'from':json.loads(str(self.from_clause)),
                'where':json.loads(str(self.where)),
                'groupby':json.loads(str(self.groupby)),
                'having':json.loads(str(self.having))
            }
        }
        
        return json.dumps(output)
        
    def getTables(self) -> List[Table]:
        return self.from_clause

    def filterWherePredicates(self, filter_fn = lambda x: True) -> List[Predicate]:
        return self.__filterPredicates(filter_fn, self.where)

    def filterHavingPredicates(self, filter_fn = lambda x: True) -> List[Predicate]:
        return self.__filterPredicates(filter_fn, self.having)

    def __filterPredicates(self, filter_fn, predicates):
        if predicates is None:
            return []

        predicate_list = []
        if PredicateOps.AND == predicates.op:
            predicate_list = predicates.operands
        else:
            predicate_list = [predicates]
        
        #list of (index, predicate) tuples
        filtered_list = []
        for i, predicate in enumerate(predicate_list):
            if filter_fn(predicate):
                filtered_list.append((i, predicate))

        return filtered_list

    def getGroupByCols(self) -> List[Column]:
        return self.groupby

    def getAllCols(self) -> List[Column]:
        return Column.AllColumns

    def getSelectCols(self) -> List[Column]:
        return self.select