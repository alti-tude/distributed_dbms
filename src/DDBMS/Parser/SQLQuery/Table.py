from DDBMS.Parser.SQLQuery.BasePrimitive import BasePrimitive


class Table(BasePrimitive):
    def __init__(self, name, alias = None) -> None:
        self.name = name
        self.alias = alias
        
        if alias is None:
            self.alias = self.name

    def to_dict(self):
        output = {
            'Table': {
                'name': self.name, 
                'alias': self.alias
            }
        }

        return output
    
    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)