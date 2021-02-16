from typing import Dict
import json

class Predicate:       
    def __init__(self, operator = None, operands = None):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        output = {
            'Predicate': {
                'operator': str(self.op), 
                'operands': json.loads(str(self.operands))
            }
        }

        return json.dumps(output)

    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)