from DDBMS.BasePrimitive import BasePrimitive
from DDBMS.Parser.SQLQuery.Column import Column

class Predicate(BasePrimitive):       
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
        
        return list(set(columns))

    def to_dict(self):
        operand_dicts = []
        for operand in self.operands:
            if isinstance(operand, BasePrimitive):
                operand_dicts.append(operand.to_dict())
            else:
                operand_dicts.append(operand)    
        
        output = {
            'Predicate': {
                'operator': self.operator, 
                'operands': operand_dicts
            }
        }

        return output

    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)

    def __hash__(self) -> int:
        return hash(repr(self))