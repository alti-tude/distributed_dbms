import json
from typing import List
from DDBMS.DataStructures.Column import Column
from DDBMS.DataStructures.Table import Table
from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, *, children = []) -> None:
        super().__init__()
        self.children = children

    def addChild(self, child) -> None:
        self.children.append(child)

    @abstractmethod
    def __repr__(self) -> str:
        output = {
            'Node': {
                'children': json.loads(str(self.children))
            }
        }

        return json.dumps(output)
        

class SelectNode(Node):
    def __init__(self, *, predicate, children = []) -> None:
        super().__init__(children=children)
        self.predicate = predicate

    def __repr__(self) -> str:
        output = {
            'Select':{
                'predicate': json.loads(str(self.predicate)),
                'children': json.loads(str(self.children))
            }
        }
        return json.dumps(output)

class ProjectNode(Node):
    def __init__(self, *, columns : List[Column], children=[]) -> None:
        super().__init__(children=children)
        self.columns = columns
    
    def __repr__(self) -> str:
        output = {
            'Project':{
                'columns': json.loads(str(self.columns)),
                'children': json.loads(str(self.children))
            }
        }
        return json.dumps(output)

class GroupbyNode(Node):
    def __init__(self, *, group_by_columns : List[Column], aggregations : List[Column], children = []) -> None:
        super().__init__(children=children)
        self.group_by_columns = group_by_columns
        self.aggregations = aggregations

    def __repr__(self) -> str:
        output = {
            'Groupby':{
                'group_by_columns': json.loads(str(self.group_by_columns)),
                'aggs': json.loads(str(self.aggregations)),
                'children': json.loads(str(self.children))
            }
        }
        return json.dumps(output)

class UnionNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

    def __repr__(self) -> str:
        output = {
            'Union':{
                'children': json.loads(str(self.children))
            }
        }
        return json.dumps(output)

class JoinNode(Node):
    def __init__(self, *, join_predicate, children = []) -> None:
        super().__init__(children=children)
        self.join_predicate = join_predicate

    def __repr__(self) -> str:
        output = {
            'Union':{
                'join_predicate': json.loads(str(self.join_predicate)),
                'children': json.loads(str(self.children))
            }
        }
        return json.dumps(output)

class CrossNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

    def __repr__(self) -> str:
        output = {
            'Cross':{
                'children': json.loads(str(self.children))
            }
        }
        return json.dumps(output)

class RelationNode(Node):
    def __init__(self, *, table : Table) -> None:
        super().__init__(children=[])
        self.table = table

    def __repr__(self) -> str:
        output = {
            'Relation':{
                'table': json.loads(str(self.table)),
                'children': json.loads(str(self.children))
            }
        }
        return json.dumps(output)
