from DDBMS.DataStructures.Table import Table
from DDBMS.DataStructures.Predicate import getPredicateObj
from DDBMS.DataStructures.Column import Column
from DDBMS.DataStructures.Symbols import Keywords

predicate = {
    'select': [Column(name="id", table="t1")],
    'from': [Table(name="t1")],
    'where': {'and': [
        {'gt': [Column(name="id", table="t1"), 3]},
        {'eq': [Column(name="a", table="t1"), Column(name="b", table="t2")]},
        {'eq': [Column(name="c", table="t1"), Column(name="b", table="t2")]},
    ]}
}

print(getPredicateObj(predicate))