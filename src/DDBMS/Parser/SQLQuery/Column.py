import json
from .Table import Table
from .Symbols import Aggregation

class Column:
    def __init__(self, name : str, table : Table, alias = None, aggregation = Aggregation.NONE) -> None:
        self.name = name
        self.table = table
        self.alias = alias
        self.aggregation = aggregation

        if alias is None:
            self.alias = self.name
        
    def __repr__(self) -> str:
        output = {
            'Column': {
                'name': str(self.name), 
                'table': str(self.table), 
                'alias': str(self.alias), 
                'agg': str(self.aggregation)
            }
        }
            
        return str(output)

    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)