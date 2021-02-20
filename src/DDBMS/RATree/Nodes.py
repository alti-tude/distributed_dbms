from typing import List
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Table import Table
from abc import ABC, abstractmethod

#TODO add a function to return the output dict as  dict (for pretty printing later)
class Node(ABC):
    def __init__(self, *, children = []) -> None:
        super().__init__()
        self.parent = None

        self.children = []
        for child in children:
            self.addChild(child)

    def addChild(self, child) -> None:
        child.parent = self
        self.children.append(child)

    @abstractmethod
    def __repr__(self) -> str:
        output = {
            'Node': {
                'children': str(self.children)
            }
        }

        return str(output)
        

class SelectNode(Node):
    def __init__(self, *, predicate, children = []) -> None:
        super().__init__(children=children)
        self.predicate = predicate

    def __repr__(self) -> str:
        output = {
            'Select':{
                'predicate': str(self.predicate),
                'children': str(self.children)
            }
        }
        return str(output)

class ProjectNode(Node):
    def __init__(self, *, columns : List[Column], children=[]) -> None:
        super().__init__(children=children)
        self.columns = columns
    
    def __repr__(self) -> str:
        output = {
            'Project':{
                'columns': str(self.columns),
                'children': str(self.children)
            }
        }
        return str(output)

class GroupbyNode(Node):
    def __init__(self, *, group_by_columns : List[Column], children = []) -> None:
        super().__init__(children=children)
        self.group_by_columns = group_by_columns

    def __repr__(self) -> str:
        output = {
            'Groupby':{
                'group_by_columns': str(self.group_by_columns),
                'children': str(self.children)
            }
        }
        return str(output)

class UnionNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

    def __repr__(self) -> str:
        output = {
            'Union':{
                'children': str(self.children)
            }
        }
        return str(output)

class JoinNode(Node):
    def __init__(self, join_predicate, children = []) -> None:
        super().__init__(children=children)
        self.join_predicate = join_predicate

    def __repr__(self) -> str:
        output = {
            'Union':{
                'join_predicate': str(self.join_predicate),
                'children': str(self.children)
            }
        }
        return str(output)

class CrossNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

    def __repr__(self) -> str:
        output = {
            'Cross':{
                'children': str(self.children)
            }
        }
        return str(output)

class RelationNode(Node):
    def __init__(self, table : Table) -> None:
        super().__init__(children=[])
        self.table = table

    def __repr__(self) -> str:
        output = {
            'Relation':{
                'table': str(self.table),
                'children': str(self.children)
            }
        }
        return str(output)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Table):
            return self.table == o
        
        return super().__eq__(o)
