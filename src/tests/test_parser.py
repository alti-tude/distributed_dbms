from DDBMS.Parser.SQLQuery import Column, SQLQuery, Table
from DDBMS.RATree.RATreeBuilder import RATreeBuilder
from DDBMS.Parser import SQLParser
import DDBMS

def test_getPredicateObj():

    predicate = SQLQuery.get().newPredicate({
        'and': [
            {'gt': [Column(name="id", table=Table(name="t1")), 3]},
            {'eq': [Column(name="a", table=Table(name="t1")), Column(name="b", table=Table(name="t2"))]},
            {'eq': [Column(name="c", table=Table(name="t1")), Column(name="b", table=Table(name="t2"))]},
        ]
    })

    target = """
        {'Predicate': {'operator': 'and', 'operands': [{'Predicate': {'operator': 'gt', 'operands': [{'Column': {'name': 'id', 'table': "{'Table': {'name': 't1', 'alias': 't1'}}", 'alias': 'id', 'agg': 'none'}}, 3]}}, {'Predicate': {'operator': 'eq', 'operands': [{'Column': {'name': 'a', 'table': "{'Table': {'name': 't1', 'alias': 't1'}}", 'alias': 'a', 'agg': 'none'}}, {'Column': {'name': 'b', 'table': "{'Table': {'name': 't2', 'alias': 't2'}}", 'alias': 'b', 'agg': 'none'}}]}}, {'Predicate': {'operator': 'eq', 'operands': [{'Column': {'name': 'c', 'table': "{'Table': {'name': 't1', 'alias': 't1'}}", 'alias': 'c', 'agg': 'none'}}, {'Column': {'name': 'b', 'table': "{'Table': {'name': 't2', 'alias': 't2'}}", 'alias': 'b', 'agg': 'none'}}]}}]}}
    """.strip()

    assert str(predicate) == target

#region Regression TEST
def test_aggregation():

    query = "select max(MovieID) from Movie;"

    SQLParser().parse(query)

    assert 1==1

#endregion  