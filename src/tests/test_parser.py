from DDBMS.DataStructures.SQLQuery import SQLQuery
from DDBMS.DataStructures import Column, Table
from DDBMS.DataStructures.Predicate import getPredicateObj
from DDBMS.RATree.RATreeBuilder import RATreeBuilder
import DDBMS
def test_getPredicateObj():

    predicate = getPredicateObj({
        'and': [
            {'gt': [Column(name="id", table=Table(name="t1")), 3]},
            {'eq': [Column(name="a", table=Table(name="t1")), Column(name="b", table=Table(name="t2"))]},
            {'eq': [Column(name="c", table=Table(name="t1")), Column(name="b", table=Table(name="t2"))]},
        ]
    })

    target = """
        and, ["gt, [\'id, t1, t1, id, none\', \'3\']", "eq, [\'a, t1, t1, a, none\', \'b, t2, t2, b, none\']", "eq, [\'c, t1, t1, c, none\', \'b, t2, t2, b, none\']"]
    """.strip()

    assert str(predicate) == target


