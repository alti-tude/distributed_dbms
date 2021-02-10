from typing import Dict
import json

class Predicate:
    def __init__(self, *, op = None, operands = None):
        self.op = op
        self.operands = operands

    def __repr__(self):
        output = {
            'Predicate': {
                'operator': str(self.op), 
                'operands': json.loads(str(self.operands))
            }
        }

        return json.dumps(output)

def buildPredicateTree(parsed_predicate : Dict) -> Predicate:
    operator = next(iter(parsed_predicate))
    operands = []
    for parsed_operand in parsed_predicate[operator]:
        if isinstance(parsed_operand, dict):
            operands.append(buildPredicateTree(parsed_operand))
        else:
            operands.append(parsed_operand)
    
    return Predicate(op = operator, operands = operands)
