from DDBMS.BasePrimitive import BasePrimitive
from .Table import Table
from .Symbols import Aggregation

class Column(BasePrimitive):
    def __init__(self, name : str, table : Table, alias = None, aggregation = Aggregation.NONE) -> None:
        self.name = name
        self.table = table
        self.alias = alias
        self.aggregation = aggregation

        if alias is None:
            self.alias = self.name
        
    def to_dict(self) :
        output = {
            'Column': {
                'name': self.name, 
                'table': self.table.to_dict() if self.table is not None else None, 
                'alias': self.alias, 
                'agg': self.aggregation
            }
        }
            
        return output
    
    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)