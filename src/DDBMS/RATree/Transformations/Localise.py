from pandas.core.frame import DataFrame
from DDBMS.Parser.SQLQuery.SQLQuery import SQLQuery
from DDBMS.RATree.RATreeBuilder import RATreeBuilder, seperateSelect
from DDBMS.Parser.SQLParser import SQLParser
from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.RATree.Nodes import HorizontalFragNode, Node, RelationNode, UnionNode
from DDBMS.DB import db

import moz_sql_parser

'''
TODO build materialisation for all frags and put in map
TODO build materialisation for all tables and put in map

TODO recurse through tree and replace leaves with materialisations

TODO call optimisations (put these as seperate files)
    union up
    TODO prune horizontal using above selects
    TODO prune derived horizontal using join criteria
    TODO prune vertical using projection
'''

@db.execute
def __getFragments(relation_name):
    #FragmentID | FragmentationType | RelationName
    return f"CALL getFragments('{relation_name}')"

#region HORIZONTAL FRAG
@db.execute
def __getHorizontalFrags(relation_name):
    #FragmentID | FragmentationType | RelationName | Predicate
    return f"CALL getHorizontalFragments('{relation_name}')"

def materialiseHorizontalFrag(fragment_details, table : Table):
    name = fragment_details['FragmentID']

    dummy_query = f"select * from temp where {fragment_details['Predicate']}".replace('"', "'")
    predicate_dict = moz_sql_parser.parse(dummy_query)['where']
    print(predicate_dict)
    predicate_dict = SQLParser().parsePredicate(predicate_dict) #convert to Columns and Tables
    processed_predicate = SQLQuery.get().newPredicate(predicate_dict) #convert to predicate object
    
    relation_node = RelationNode(table)
    select_seperated = seperateSelect(processed_predicate, relation_node)

    return HorizontalFragNode(name, table, processed_predicate, children=[select_seperated])

#endregion


def materialiseTable(table : Table):
    frag_types : DataFrame = __getFragments(table.name)

    if frag_types.iloc[0]['FragmentationType'] == 'H':
        frags = []
        frag_details : DataFrame = __getHorizontalFrags(table.name)
        for idx, frag_detail in frag_details.iterrows():
            frags.append(materialiseHorizontalFrag(frag_detail, table))

        return UnionNode(children=frags)

def materialiseAllTables(node : Node):
    if isinstance(node, RelationNode):
        new_node = materialiseTable(node.table)
        parent : Node = node.parent
        if parent is None:
            new_node.makeRoot()
        else:
            parent.replaceChild(node, new_node)
        
        return new_node
    
    for child in node.children:
        materialiseAllTables(child)
    
    return node