from DDBMS.DataStructures.Aggregation import Aggregation
from DDBMS.DataStructures.Table import Table

class Column:
    def __init__(self, *, name, table, alias = None, aggregation = Aggregation.NONE) -> None:
        self.name = name
        self.table = table
        self.alias = alias
        self.aggregation = aggregation

        if alias is None:
            self.alias = self.name