from DDBMS.DataStructures.Table import Table
from DDBMS.DataStructures.Symbols import Aggregation

class Column:
    def __init__(self, *, name : str, table : Table, alias = None, aggregation = Aggregation.NONE) -> None:
        self.name = name
        self.table = table
        self.alias = alias
        self.aggregation = aggregation

        if alias is None:
            self.alias = self.name

    def __repr__(self) -> str:
        return f"{self.name}, {self.table}, {self.alias}, {self.aggregation}"