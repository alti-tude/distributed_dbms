from DDBMS.DataStructures.Aggregation import Aggregation


class Column:
    def __init__(self, *, name, table, alias = None, aggregation = Aggregation.NONE) -> None:
        self.name = name
        self.table = table
        self.alias = alias
        self.aggregation = aggregation