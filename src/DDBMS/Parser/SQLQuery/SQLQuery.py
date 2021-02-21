from .Predicate import Predicate
from .Column import Column
from .Table import Table
from .Symbols import *

class SQLQuery:
    #TODO move this to a store object
    INSTANCE = None

    @classmethod
    def get(cls):
        if cls.INSTANCE is not None:
            return cls.INSTANCE
        
        cls.INSTANCE = cls()
        return cls.INSTANCE

    @classmethod
    def reset(cls):
        cls.INSTANCE = cls()
        return cls.INSTANCE

    def __init__(self):
        self.columns = []
        self.tables = []
        self.predicates = []

        self.select = []
        self.where = []
        self.groupby = []
        self.having = []

    def addFrom(self, table):
        for old_table in self.tables:
            if table == old_table:
                return
        
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

    def newTable(self, name, alias = None):
        new_table = Table(name, alias)
        for old_table in self.tables:
            if new_table == old_table:
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
    
    def filterCols(self, name = None, alias = None, table : Table = None, aggregation = None):
        cols = self.columns
        cols = list(filter(lambda col : col.name == name or name is None, cols))
        cols = list(filter(lambda col : col.alias == alias or alias is None, cols))
        cols = list(filter(lambda col : col.table is table or table is None, cols))
        cols = list(filter(lambda col : col.aggregation == aggregation or aggregation is None, cols))

        return cols

    def __repr__(self) -> str:
        output = {
            "columns" : self.columns,
            "tables" : self.tables,
            "predicates" : self.predicates,

            "select" : self.select,
            "where" : self.where,
            "groupby" : self.groupby,
            "having" : self.having
        }

        return str(output)