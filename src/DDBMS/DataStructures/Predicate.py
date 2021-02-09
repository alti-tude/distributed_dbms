from typing import Dict

class Predicate:
    def __init__(self, *, op = None, operands = None):
        self.op = op
        self.operands = operands

    def __str__(self):
        return f"{self.op}, {[str(operand) for operand in self.operands]}"

def getPredicateObj(parsed_predicate : Dict) -> Predicate:
    operator = next(iter(parsed_predicate))
    operands = []
    for parsed_operand in parsed_predicate[operator]:
        if isinstance(parsed_operand, dict):
            operands.append(getPredicateObj(parsed_operand))
        else:
            operands.append(parsed_operand)
    
    return Predicate(op = operator, operands = operands)
