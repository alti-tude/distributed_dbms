from copy import copy, deepcopy
from DDBMS.BasePrimitive import BasePrimitive
from typing import List
from DDBMS.Parser.SQLQuery import Column, Table, Predicate
from treelib import Tree

class Node(BasePrimitive):
    def __init__(self, *, children = []) -> None:
        super().__init__()
        self.parent : Node = None

        self.children = []
        for child in children:
            self.addChild(child)

        
    def makeRoot(self):
        self.parent = None
        
    def addChild(self, child) -> None:
        child.parent = self
        self.children.append(child)

    def getChildId(self, query_child):
        for i, child in enumerate(self.children):
            if query_child is child:
                return i
            
        return -1

    def replaceChildById(self, idx, new_child):
        old_child = self.children[idx]
        new_child.parent = self
        self.children[idx] = new_child
        return old_child

    def replaceChild(self, old_child, new_child):
        idx = self.getChildId(old_child)
        assert idx != -1, f"Can't replace {type(old_child)}: child does not exist"
        return self.replaceChildById(idx, new_child)

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

    def copy(self):
        # cls = type(self)
        new_obj : Node = copy(self)
        new_obj.children = []
        for child in self.children:
            new_obj.addChild(child.copy())
        return new_obj
    
    def to_treelib(self, tree : Tree, is_root=False):
        tree.create_node(
            tag = f"{self.compact_display()}", 
            identifier=str(id(self)), 
            parent=str(id(self.parent)) if self.parent is not None and not is_root else None
        )

        for child in self.children:
            child.to_treelib(tree)
    
class SelectNode(Node):
    def __init__(self, *, predicate, children = []) -> None:
        super().__init__(children=children)
        self.predicate : Predicate = predicate

    def to_dict(self):
        output = {
            'Select':{
                'predicate': self.predicate.to_dict(),
                'children': [child.to_dict() for child in self.children]
            }
        }
        return output
    
    def compact_display(self):
        return "SELECT: " + self.predicate.compact_display()

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
    
    def compact_display(self):
        columns_str = ""
        for column in self.columns:
            if columns_str != "":
                columns_str += ", "
            columns_str += column.compact_display()

        return "PROJECT: " + columns_str


class FinalProjectNode(Node):
    def __init__(self, *, columns : List[Column], children=[]) -> None:
        super().__init__(children=children)
        self.columns = columns
    
    def to_dict(self):
        output = {
            'FinalProject':{
                'columns': [column.to_dict() for column in self.columns],
                'children': [child.to_dict() for child in self.children]
            }
        }
        return output
    
    def compact_display(self):
        columns_str = ""
        for column in self.columns:
            if columns_str != "":
                columns_str += ", "
            columns_str += column.compact_display()

        return "FINAL PROJECT: " + columns_str

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

    def compact_display(self):
        columns_str = ""
        for column in self.group_by_columns:
            if columns_str != "":
                columns_str += ", "
            columns_str += column.compact_display()

        return "GROUP BY: " + columns_str


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
    
    def compact_display(self):
        return "UNION"

class JoinNode(Node):
    def __init__(self, join_predicate, children = []) -> None:
        super().__init__(children=children)
        self.join_predicate : Predicate= join_predicate

    def to_dict(self):
        output = {
            'Join':{
                'join_predicate': self.join_predicate.to_dict(),
                'children': [child.to_dict() for child in self.children]
            }
        }
        
        return output
    
    def compact_display(self):
        return "JOIN: " + self.join_predicate.compact_display()


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
    
    def compact_display(self):
        return "CROSS"

class RelationNode(Node):
    def __init__(self, table : Table, children = []) -> None:
        super().__init__(children=children)
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
    
    def compact_display(self):
        return "RELATION: " + self.table.compact_display()

class HorizontalFragNode(RelationNode):
    def __init__(self, name, table: Table, predicate : Predicate, children = []) -> None:
        super().__init__(table, children)
        self.name = name
        self.predicate = predicate
    
    def to_dict(self):
        return {
            "HorizontalFragNode":{
                "name": self.name,
                "table": self.table.to_dict(),
                "predicate": self.predicate.to_dict(),
                "children": [child.to_dict() for child in self.children]
            }
        }
    
    def compact_display(self):
        return "HORIZONTAL FRAGMENT: " + self.name

class VerticalFragNode(RelationNode):
    def __init__(self, name, table: Table, columns = [], children = []) -> None:
        super().__init__(table, children)
        self.name = name
        self.columns = columns
    
    def to_dict(self):
        return {
            "VerticalFragNode":{
                "name": self.name,
                "table": self.table.to_dict(),
                "columns": [column.to_dict() for column in self.columns],
                "children": [child.to_dict() for child in self.children]
            }
        }

    def compact_display(self):
        return "VERTICAL FRAGMENT: " + self.name

class DerivedHorizontalFragNode(RelationNode):
    def __init__(self, table: Table, left_frag_name, right_frag_name, join_predicate, children = []) -> None:
        super().__init__(table, children)
        self.left_frag_name = left_frag_name
        self.right_frag_name = right_frag_name
        self.join_predicate : Predicate = join_predicate
    
    def to_dict(self):
        return {
            "DerivedHorizontalFragNode":{
                "left_frag_name": self.left_frag_name,
                "right_frag_name": self.right_frag_name,
                "join_predicate": self.join_predicate.to_dict(),
                "children": [child.to_dict() for child in self.children]
            }
        }
    
    def compact_display(self):
        return "DERIVED HORIZONTAL FRAGMENT: " + self.left_frag_name
