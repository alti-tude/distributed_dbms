from DDBMS.DataStructures.SQLQuery import SQLQuery
from DDBMS.DataStructures import Column, Table
from DDBMS.DataStructures.Predicate import getPredicateObj
from DDBMS.RATree.RATreeBuilder import RATreeBuilder
import DDBMS

def test_joinLeaves(mocker):
    sql =  {
            'select': [Column(name="id", table=Table(name="t1"))],
            'from': [Table(name="t1"), Table(name="t2"), Table(name="t3"), Table(name="t4")],
            'where': {'and': [
                {'gt': [Column(name="id", table=Table(name="t1")), 3]},
                {'or':[
                    {'eq': [Column(name="a", table=Table(name="t1")), Column(name="b", table=Table(name="t2"))]},
                    {'eq': [Column(name="a", table=Table(name="t1")), Column(name="b", table=Table(name="t4"))]}
                ]},
                {'eq': [Column(name="a", table=Table(name="t1")), Column(name="b", table=Table(name="t3"))]},
                {'eq': [Column(name="c", table=Table(name="t2")), Column(name="b", table=Table(name="t3"))]},
            ]}
        }
    with mocker.patch.object(DDBMS.DataStructures.SQLQuery, 'parseSql', return_value = sql):
        tmp = SQLQuery(query_string= "whatever")
        builder = RATreeBuilder(tmp)
        
    assert 1==1
