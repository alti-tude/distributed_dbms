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
        and, ["gt, ['id, t1, id, 0', '3']", "eq, ['a, t1, a, 0', 'b, t2, b, 0']", "eq, ['c, t1, c, 0', 'b, t2, b, 0']"]
    """.strip()

    assert str(predicate) == target


