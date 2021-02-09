from typing import List
from DDBMS.DataStructures.Column import Column
from DDBMS.DataStructures.Table import Table
from abc import ABC, abstractmethod

class Node():
    def __init__(self, *, children = []) -> None:
        self.children = children

    def addChild(self, child) -> None:
        self.children.append(child)

    # @abstractmethod
    # def postOrder(self, visitor):
    #     visitor.visit(self)
    #     for child in self.children:
    #         visitor.visi
    
class SelectNode(Node):
    def __init__(self, *, predicate, children = []) -> None:
        super().__init__(children=children)
        self.predicate = predicate

class ProjectNode(Node):
    def __init__(self, *, columns : List[Column], children=[]) -> None:
        super().__init__(children=children)
        self.columns = columns
    
class GroupbyNode(Node):
    def __init__(self, *, group_by_columns : List[Column], aggregations, children = []) -> None:
        super().__init__(children=children)
        self.group_by_columns = group_by_columns
        self.aggregations = aggregations

class UnionNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

class JoinNode(Node):
    def __init__(self, *, join_predicate, children = []) -> None:
        super().__init__(children=children)
        self.join_predicate = join_predicate

class CrossNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

class RelationNode(Node):
    def __init__(self, *, table : Table, children = []) -> None:
        super().__init__(children=children)
        self.table = table