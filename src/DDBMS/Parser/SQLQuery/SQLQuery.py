from DDBMS.Parser.SQLQuery.Predicate import Predicate
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
        self.where = new_predicate
        return new_predicate

    def addHavingPredicate(self, predicate_dict):
        new_predicate = self.newPredicate(predicate_dict)
        self.having = new_predicate
        return new_predicate


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

    def newPredicate(self, predicate_dict):
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
        
