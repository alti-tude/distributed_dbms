class Table:
    def __init__(self, *, name, alias = None) -> None:
        self.name = name
        self.alias = alias
        
        if alias is None:
            self.alias = self.name

    def __str__(self):
        return f"{self.name}, {self.alias}"