#TODO modify all these according to moz-sql
class Aggregation:
    NONE = "none"
    MAX = "max"

class PredicateOps:
    AND = "and"
    OR = "or"
    EQ = "eq"
    GEQ = "geq"
    GT = "gt"
    LEQ = "leq"
    LT = "lt"
    NEQ = "neq"
    NOT = "not"

    @staticmethod
    def flip(op):
        if op == PredicateOps.AND: return PredicateOps.OR
        if op == PredicateOps.OR: return PredicateOps.AND
        if op == PredicateOps.EQ: return PredicateOps.NEQ
        if op == PredicateOps.NEQ: return PredicateOps.EQ
        if op == PredicateOps.GEQ: return PredicateOps.LEQ
        if op == PredicateOps.LEQ: return PredicateOps.GEQ
        if op == PredicateOps.GT: return PredicateOps.LT
        if op == PredicateOps.LT: return PredicateOps.GT
        return op

            
class Keywords:
    SELECT = "select"
    FROM = "from"
    WHERE = "where"
    GROUPBY = "groupby"
    HAVING = "having"
