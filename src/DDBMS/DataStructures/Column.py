import json
from DDBMS.DataStructures.Table import Table
from DDBMS.DataStructures.Symbols import Aggregation

class Column:
    AllColumns = []
    def __init__(self, *, name : str, table : Table, alias = None, aggregation = Aggregation.NONE) -> None:
        self.name = name
        self.table = table
        self.alias = alias
        self.aggregation = aggregation

        if alias is None:
            self.alias = self.name
        
        Column.AllColumns.append(self)

    def __repr__(self) -> str:
        output = {
            'Column': {
                'name': str(self.name), 
                'table': json.loads(str(self.table)), 
                'alias': str(self.alias), 
                'agg': str(self.aggregation)
            }
        }
            
        return json.dumps(output)