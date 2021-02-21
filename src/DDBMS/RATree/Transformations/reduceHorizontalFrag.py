from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Symbols import PredicateOps
from DDBMS.Parser.SQLQuery import Predicate
from DDBMS.RATree.Nodes import CrossNode, HorizontalFragNode, JoinNode, ProjectNode, RelationNode, SelectNode, Node, UnionNode

def swap(a, b):
    return b,a

def __comparePred(pred1 : Predicate, pred2 : Predicate) -> bool:
    if pred2.operands == PredicateOps.AND or pred2.operands == PredicateOps.OR:
        pred1, pred2 = swap(pred1, pred2)

    if pred1.operator == PredicateOps.AND:
        for operand in pred1.operands:
            if not __comparePred(operand, pred2):
                return False

        return True
    
    if pred1.operator == PredicateOps.OR:
        for operand in pred1.operands:
            if __comparePred(operand, pred2):
                return True
        
        return False

    
    #region 2+2 column cases
    if isinstance(pred1.operands[0], Column) and isinstance(pred1.operands[1], Column) and\
        isinstance(pred2.operands[0], Column) and isinstance(pred2.operands[1], Column):

        if len(set(pred1.operands).intersection(set(pred2.operands))) != 2:
            return True
        
        operands1 = list(set(pred1.operands))
        operands2 = list(set(pred2.operands))
        #TODO finish these cases
        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.NEQ:
            return False
        if pred1.operator == PredicateOps.GT and (pred2.operator == PredicateOps.LT or pred2.operator == PredicateOps.LEQ):
            return pred1.operands[1] != pred2.operands[1]
        if pred1.operator == PredicateOps.GT and (pred2.operator == PredicateOps.LT or pred2.operator == PredicateOps.LEQ):
            return pred1.operands[1] != pred2.operands[1]
        if pred1.operator == PredicateOps.LT and (pred2.operator == PredicateOps.GT or pred2.operator == PredicateOps.GEQ):
            return pred1.operands[1] != pred2.operands[1]
        

        if pred1.operator == PredicateOps.EQ and pred2.operator == PredicateOps.NEQ:
            return False


    # region 2 + 1 column cases
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
    if isinstance(pred1.operands[1], Column): pred1.operands = list(swap(*pred1.operand))
    if isinstance(pred2.operands[1], Column): pred2.operands = list(swap(*pred2.operand))

    if pred1.operands[0] != pred2.operands[0]: return True
    
    #TODO Handle not

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

def __checkFrag(frag : HorizontalFragNode) -> bool:
    node = frag
    while node.parent is not None and \
        ( isinstance(node.parent, ProjectNode) or isinstance(node.parent, SelectNode) ):

        if isinstance(node.parent, SelectNode):
            if not __comparePred(node.parent.predicate, frag.predicate):
                return False
        
        node = node.parent

    return True


def __deleteHorizontalFrag(node : Node) -> bool:
    """[summary]

    Args:
        node (Node): [description]

    Returns:
        bool: [return True if delete branch]
    """
    
    if isinstance(node, HorizontalFragNode):
        return not __checkFrag(node)
    
    if isinstance(node, RelationNode):
        return False

    to_delete = []
    delete = False
    for child in node.children:
        if __deleteHorizontalFrag(child): 
            to_delete.append(child)
            delete = True

    for child in to_delete:
        node.deleteChild(child)
    
    #return false if not deletable
    if not ( isinstance(node, ProjectNode) or isinstance(node, SelectNode) ):
        return False
    
    return delete

def reduceHorizontalFrag(node : Node) -> Node:
    if __deleteHorizontalFrag(node):
        return None

    return node
