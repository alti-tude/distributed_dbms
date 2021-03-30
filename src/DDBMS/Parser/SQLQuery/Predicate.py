from typing import List
from DDBMS.Parser.SQLQuery.Symbols import PredicateOps
from DDBMS.BasePrimitive import BasePrimitive
from DDBMS.Parser.SQLQuery.Column import Column


class Predicate(BasePrimitive):       
    def __init__(self, operator = None, operands = None):
        self.operator = operator
        self.operands : List = operands

    def getAllColumns(self):
        columns = []
        for operand in self.operands:
            if isinstance(operand, Column):
                columns.append(operand)
            if isinstance(operand, Predicate):
                columns.extend(operand.getAllColumns())
        
        return list(set(columns))

    def predicateOperatorToSQLOperator(self):
        if self.operator == PredicateOps.EQ:
            return "="
        elif self.operator == PredicateOps.GEQ:
            return ">="
        elif self.operator == PredicateOps.GT:
            return ">"
        elif self.operator == PredicateOps.LEQ:
            return "<="
        elif self.operator == PredicateOps.LT:
            return ">"
        elif self.operator == PredicateOps.NEQ:
            return "!="  
        return self.operator
    
    #TODO display NOT differently
    def compact_display(self):
        compact_str = "("
        for operand in self.operands:
            if compact_str != "(":
                compact_str += " " + self.predicateOperatorToSQLOperator() + ' '
            if not isinstance(operand, Predicate) and \
               not isinstance(operand, Column):
                if isinstance(operand, str):
                    compact_str += f"'{operand}'"
                else:
                    compact_str += f"{operand}"
            else:
                compact_str += operand.compact_display()

        return compact_str + ')'

    def to_dict(self):
        operand_dicts = []
        for operand in self.operands:
            if isinstance(operand, BasePrimitive):
                operand_dicts.append(operand.to_dict())
            else:
                operand_dicts.append(operand)    
        
        output = {
            'Predicate': {
                'operator': self.operator, 
                'operands': operand_dicts
            }
        }

        return output

    def __eq__(self, o: object) -> bool:
        if self.operator == PredicateOps.EQ or self.operator == PredicateOps.NEQ and self.operator == PredicateOps.OR and self.operator == PredicateOps.AND:
            for operand in self.operands:
                if operand not in o.operands:
                    return False
            
            return True
            
        return repr(self) == repr(o)

    def __hash__(self) -> int:
        return hash(repr(self))


def checkNonExclusivePredicate(pred1 : Predicate, pred2 : Predicate) -> bool:
    if pred2.operator == PredicateOps.AND or pred2.operator == PredicateOps.OR:
        pred1, pred2 = pred2, pred1

    if pred1.operator == PredicateOps.AND:
        for operand in pred1.operands:
            if not checkNonExclusivePredicate(operand, pred2):
                return False

        return True
    
    if pred1.operator == PredicateOps.OR:
        for operand in pred1.operands:
            if checkNonExclusivePredicate(operand, pred2):
                return True
        
        return False

    
    #region 2 + 2 column cases
    if isinstance(pred1.operands[0], Column) and isinstance(pred1.operands[1], Column) and\
        isinstance(pred2.operands[0], Column) and isinstance(pred2.operands[1], Column):

        if len(set(pred1.operands).intersection(set(pred2.operands))) != 2:
            return True
        
        #align columns
        if pred1.operands[1] != pred2.operands[1]:
            pred2.operator = PredicateOps.flip(pred2.operator)
            pred2.operands = list(reversed(pred2.operands))

        #region EQ
        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.EQ:
            return True
        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.GEQ:
            return True
        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.GT:
            return False
        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.LEQ:
            return True
        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.LT:
            return False
        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.NEQ:
            return False
        #endregion

        #region GEQ
        if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.EQ:
            return True
        if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.GEQ:
            return True
        if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.GT:
            return True
        if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.LEQ:
            return True
        if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.LT:
            return False
        if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.NEQ:
            return True
        #endregion

        #region GT
        if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.EQ:
            return False
        if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.GEQ:
            return True
        if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.GT:
            return True
        if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.LEQ:
            return False
        if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.LT:
            return False
        if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.NEQ:
            return True
        #endregion

        #region LEQ
        if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.EQ:
            return True
        if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.GEQ:
            return True
        if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.GT:
            return False
        if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.LEQ:
            return True
        if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.LT:
            return True
        if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.NEQ:
            return True
        #endregion

        #region LT
        if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.EQ:
            return False
        if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.GEQ:
            return False
        if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.GT:
            return False
        if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.LEQ:
            return True
        if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.LT:
            return True
        if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.NEQ:
            return True
        #endregion

        #region NEQ
        if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.EQ:
            return False
        if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.GEQ:
            return True
        if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.GT:
            return True
        if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.LEQ:
            return True
        if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.LT:
            return True
        if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.NEQ:
            return True
        #endregion
        
    #endregion

    #region 2 + 1 column cases
    if isinstance(pred1.operands[0], Column) and isinstance(pred1.operands[1], Column) and\
        isinstance(pred2.operands[0], Column) and not isinstance(pred2.operands[1], Column):
        return True

    if isinstance(pred1.operands[0], Column) and isinstance(pred1.operands[1], Column) and\
        not isinstance(pred2.operands[0], Column) and isinstance(pred2.operands[1], Column):
        return True

    if not isinstance(pred1.operands[0], Column) and isinstance(pred1.operands[1], Column) and\
        isinstance(pred2.operands[0], Column) and isinstance(pred2.operands[1], Column):
        return True

    if isinstance(pred1.operands[0], Column) and not isinstance(pred1.operands[1], Column) and\
        isinstance(pred2.operands[0], Column) and isinstance(pred2.operands[1], Column):
        return True
    #endregion

    #region only 1 column cases
    #bring all columns to index 0
    if isinstance(pred1.operands[1], Column): 
        pred1.operands = list(reversed(pred1.operand))
        pred1.operator = PredicateOps.flip(pred1.operator)

    if isinstance(pred2.operands[1], Column): 
        pred2.operands = list(reversed(pred2.operand))
        pred2.operator = PredicateOps.flip(pred2.operator)

    #if the column is not same, then valid
    if pred1.operands[0] != pred2.operands[0]: return True
    

    #region EQ
    if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.EQ:
        return pred1.operands[1] == pred2.operands[1]
    
    if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.GT:
        return pred1.operands[1] > pred2.operands[1]
    
    if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.LT:
        return pred1.operands[1] < pred2.operands[1]
    
    if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.GEQ:
        return pred1.operands[1] >= pred2.operands[1]
    
    if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.LEQ:
        return pred1.operands[1] <= pred2.operands[1]
    
    if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.NEQ:
        return pred1.operands[1] != pred2.operands[1]
    
    #endregion

    #region GEQ
    if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.EQ:
        return pred1.operands[1] <= pred2.operands[1]
    
    if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.GEQ:
        return True

    if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.GT:
        return True

    if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.LEQ:
        return pred1.operands[1] <= pred2.operands[1]

    if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.LT:
        return pred1.operands[1] < pred2.operands[1]
    
    if pred1.operator == PredicateOps.GEQ and pred2.operator == PredicateOps.NEQ:
        return True
    
    #endregion

    #region GT
    if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.EQ:
        return pred1.operands[1] < pred2.operands[1]
    
    if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.GEQ:
        return True

    if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.GT:
        return True

    if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.LEQ:
        return pred1.operands[1] < pred2.operands[1]

    if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.LT:
        if isinstance(pred1.operands[1], int):
            return pred1.operands[1] < pred2.operands[1] - 1
        return pred1.operands[1] < pred2.operands[1]
    
    if pred1.operator == PredicateOps.GT and pred2.operator == PredicateOps.NEQ:
        return True
    
    #endregion

    #region LEQ
    if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.EQ:
        return pred1.operands[1] >= pred2.operands[1]
    
    if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.GEQ:
        return pred1.operands[1] >= pred2.operands[1]

    if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.GT:
        return pred1.operands[1] > pred2.operands[1]

    if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.LEQ:
        return True

    if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.LT:
        return True
    
    if pred1.operator == PredicateOps.LEQ and pred2.operator == PredicateOps.NEQ:
        return True
    
    #endregion

    #region LT

    if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.EQ:
        return pred1.operands[1] > pred2.operands[1]
    
    if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.GEQ:
        return pred1.operands[1] > pred2.operands[1]

    if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.GT:
        if isinstance(pred1.operands[1], int):
            return pred1.operands[1] - 1 > pred2.operands[1]
        return pred1.operands[1] > pred2.operands[1]

    if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.LEQ:
        return True

    if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.LT:
        return True
    
    if pred1.operator == PredicateOps.LT and pred2.operator == PredicateOps.NEQ:
        return True
    #endregion

    #region NEQ
    if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.EQ:
        return pred1.operands[1] != pred2.operands[1]
    
    if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.GT:
        return True
    
    if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.LT:
        return True
    
    if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.GEQ:
        return True
    
    if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.LEQ:
        return True
    
    if pred1.operator == PredicateOps.NEQ and pred2.operator == PredicateOps.NEQ:
        return True
    #endregion

    #endregion

    raise Exception("operator no implemented")
