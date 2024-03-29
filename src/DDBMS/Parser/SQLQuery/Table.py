import json


class Table:
    def __init__(self, name, alias = None) -> None:
        self.name = name
        self.alias = alias
        
        if alias is None:
            self.alias = self.name

    def __repr__(self):
        output = {
            'Table': {
                'name': str(self.name), 
                'alias': str(self.alias)
            }
        }

        return str(output)
    
    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)