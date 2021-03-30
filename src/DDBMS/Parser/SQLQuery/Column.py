from DDBMS.BasePrimitive import BasePrimitive
from .Table import Table
from .Symbols import Aggregation
from DDBMS.DB.DBUtils import getDataType

class Column(BasePrimitive):
    def __init__(self, name : str, table : Table, alias = None, aggregation = Aggregation.NONE) -> None:
        self.name = name
        self.table = table
        self.alias = alias
        self.aggregation = aggregation
        self.data_type = str(getDataType(self.name, self.table.name).iloc[0]["DataType"])
        

        if alias is None:
            self.alias = self.name
        
    def to_dict(self) :
        output = {
            'Column': {
                'name': self.name, 
                'table': self.table.to_dict() if self.table is not None else None, 
                'alias': self.alias, 
                'agg': self.aggregation,
                'data_type': self.data_type
            }
        }
            
        return output
    
    def compact_display(self, table=None):
        compact_str = ""
        
        if self.aggregation != Aggregation.NONE:
            compact_str += self.aggregation + '('
        
        if table is None:
            compact_str += f"`{self.table.alias}`."
        else:
            compact_str += f"`{table.alias}`."

        compact_str += self.name
        if self.aggregation != Aggregation.NONE:
            compact_str += ')'
        
        if self.alias != self.name:
            compact_str += " as " + self.alias
        
        return compact_str


