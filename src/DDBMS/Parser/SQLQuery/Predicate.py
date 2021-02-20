from DDBMS.Parser.SQLQuery.Column import Column
from typing import Dict
import json

class Predicate:       
    def __init__(self, operator = None, operands = None):
        self.operator = operator
        self.operands = operands

    def getAllColumns(self):
        columns = []
        for operand in self.operands:
            if isinstance(operand, Column):
                columns.append(operand)
            if isinstance(operand, Predicate):
                columns.extend(operand.getAllColumns())
        
        return columns

    def __repr__(self):
        output = {
            'Predicate': {
                'operator': str(self.operator), 
                'operands': self.operands
            }
        }

        return str(output)

    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)

    def __hash__(self) -> int:
        return hash(repr(self))