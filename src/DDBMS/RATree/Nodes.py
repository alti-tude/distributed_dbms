from DDBMS.BasePrimitive import BasePrimitive
from typing import List
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Table import Table
from abc import ABC, abstractmethod

#TODO add a function to return the output dict as  dict (for pretty printing later)
class Node(BasePrimitive):
    def __init__(self, *, children = []) -> None:
        super().__init__()
        self.parent = None

        self.children = []
        for child in children:
            self.addChild(child)

    def addChild(self, child) -> None:
        child.parent = self
        self.children.append(child)

    def getChildId(self, query_child):
        for i, child in enumerate(self.children):
            if query_child is child:
                return i
            
        return -1

    def replaceChild(self, old_child, new_child):
        idx = self.getChildId(old_child)
        assert idx != -1, f"Can't replace {old_child}: child does not exist"
        self.children[idx] = new_child
        return new_child

    def deleteChild(self, child):
        idx = self.getChildId(child)
        if idx != -1:
            return self.children.pop(idx)
        
        return child
    
    def childExists(self, child):
        return self.getChildId(child) != -1

    def to_dict(self):
        output = {
            'Node': {
                'children': str(self.children)
            }
        }

        return output

    def __hash__(self) -> int:
        return hash(repr(self))
    
    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)

class SelectNode(Node):
    def __init__(self, *, predicate, children = []) -> None:
        super().__init__(children=children)
        self.predicate = predicate

    def to_dict(self):
        output = {
            'Select':{
                'predicate': self.predicate.to_dict(),
                'children': [child.to_dict() for child in self.children]
            }
        }
        return output

class ProjectNode(Node):
    def __init__(self, *, columns : List[Column], children=[]) -> None:
        super().__init__(children=children)
        self.columns = columns
    
    def to_dict(self):
        output = {
            'Project':{
                'columns': [column.to_dict() for column in self.columns],
                'children': [child.to_dict() for child in self.children]
            }
        }
        return output

class GroupbyNode(Node):
    def __init__(self, *, group_by_columns : List[Column], children = []) -> None:
        super().__init__(children=children)
        self.group_by_columns = group_by_columns

    def to_dict(self):
        output = {
            'Groupby':{
                'group_by_columns': [column.to_dict() for column in self.group_by_columns],
                'children': [child.to_dict() for child in self.children]
            }
        }
        
        return output

class UnionNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

    def to_dict(self):
        output = {
            'Union':{
                'children': [child.to_dict() for child in self.children]
            }
        }
        return output

class JoinNode(Node):
    def __init__(self, join_predicate, children = []) -> None:
        super().__init__(children=children)
        self.join_predicate = join_predicate

    def to_dict(self):
        output = {
            'Join':{
                'join_predicate': self.join_predicate.to_dict(),
                'children': [child.to_dict() for child in self.children]
            }
        }
        
        return output
        

class CrossNode(Node):
    def __init__(self, *, children = []) -> None:
        super().__init__(children=children)

    def to_dict(self):
        output = {
            'Cross':{
                'children': [child.to_dict() for child in self.children]
            }
        }
        
        return output

class RelationNode(Node):
    def __init__(self, table : Table) -> None:
        super().__init__(children=[])
        self.table = table

    def to_dict(self):
        output = {
            'Relation':{
                'table': self.table.to_dict(),
                'children': [child.to_dict() for child in self.children]
            }
        }

        return output

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Table):
            return self.table == o
        
        return super().__eq__(o)
