from typing import List
from .Predicate import Predicate
from .Column import Column
from .Table import Table
from .Symbols import *

class SQLQuery:       
    def __init__(self):
        self.columns = []
        self.tables = []
        self.predicates = []

        self.select = []
        self.where = None
        self.join = None
        self.groupby = []
        self.having = None

    def addFrom(self, table):
        self.tables.append(table)
    
    def addSelectColumn(self, name : str, table : Table, alias = None, aggregation = Aggregation.NONE):
        new_col = self.newColumn(name, table, alias, aggregation)
        self.select.append(new_col)
        return new_col
    
    def addGroupbyColumn(self, name : str, table : Table, alias = None, aggregation = Aggregation.NONE):
        new_col = self.newColumn(name, table, alias, aggregation)
        self.groupby.append(new_col)
        return new_col

    def addWherePredicate(self, predicate_dict):
        new_predicate = self.newPredicate(predicate_dict)
        if new_predicate.operator == PredicateOps.AND:
            self.where = new_predicate.operands
        else: 
            self.where = [new_predicate]
        return self.where

    def addHavingPredicate(self, predicate_dict):
        new_predicate = self.newPredicate(predicate_dict)
        if new_predicate.operator == PredicateOps.AND:
            self.having = new_predicate.operands
        else: 
            self.having = [new_predicate]
        return self.having

    def newTable(self, name, alias):
        new_table = Table(name, alias)
        for old_table in self.tables:
            if repr(new_table) == repr(old_table):
                return old_table
        
        self.tables.append(new_table)
        return new_table

    def newColumn(self, name : str, table : Table, alias = None, aggregation = Aggregation.NONE):
        new_col = Column(name, table, alias, aggregation)
        for old_col in self.columns:
            if repr(new_col) == repr(old_col):
                return old_col
        
        self.columns.append(new_col)
        return new_col

    def newPredicate(self, predicate_dict) -> Predicate:
        operator = next(iter(predicate_dict))
        operands = []
        for operand_dict in predicate_dict[operator]:
            if isinstance(operand_dict, dict):
                operands.append(self.newPredicate(operand_dict))
            else:
                operands.append(operand_dict)

        new_predicate = Predicate(operator = operator, operands = operands)
        for old_predicate in self.predicates:
            if repr(new_predicate) == repr(old_predicate):
                return old_predicate
        
        self.predicates.append(new_predicate)
        return new_predicate
    
    def __equalPredicateMask(self) -> List[bool]:
        mask = [False for _ in self.where]
        for i, predicate in enumerate(self.where):
            if  predicate.operator == PredicateOps.EQ and \
                len(predicate.operands) == 2 and \
                isinstance(predicate.operands[0], Column) and \
                isinstance(predicate.operands[1], Column) and \
                predicate.operands[0].table.alias != predicate.operands[1].table.alias:
                mask[i] = True
        return mask

    def __joinPredicatesMask(self, mask) -> List[bool]:
        class DSU:
            def __init__(self, size) -> None:
                self.parent = [i for i in range(size)]

            def root(self, node):
                if self.parent[node] == node: return node
                root = self.root(self.parent[node])
                self.parent[node] = root
                return root
            
            def merge(self, u, v):
                self.parent[self.root(u)] = self.root(v)

        
        dsu = DSU(len(self.tables))

        for idx, selected in enumerate(mask):
            if not selected: continue
            
            left_index = self.tables.index(self.where[idx].operands[0].table)
            right_index = self.tables.index(self.where[idx].operands[1].table)
            if dsu.root(left_index) == dsu.root(right_index): 
                mask[idx] = False
                continue

            mask[idx] = True
            dsu.merge(left_index, right_index)

        return mask            

    def __orderJoinPredicates(self):
        #TODO order self.join
        pass

    def buildJoin(self):
        if self.join is not None:
            return self.join

        mask = self.__equalPredicateMask()
        mask = self.__joinPredicatesMask(mask)

        where_copy = self.where
        self.join = [where_copy[idx] for idx in range(len(mask)) if mask[idx]]
        self.__orderJoinPredicates()
        self.where = [where_copy[idx] for idx in range(len(mask)) if not mask[idx]]

        return self.join

