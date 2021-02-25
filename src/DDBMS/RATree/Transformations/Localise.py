from pandas.core.frame import DataFrame
from DDBMS.Parser.SQLQuery.Symbols import Aggregation, Keywords, PredicateOps
from DDBMS.Parser.SQLQuery.SQLQuery import SQLQuery
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.RATree.RATreeBuilder import RATreeBuilder, seperateSelect
from DDBMS.Parser.SQLParser import SQLParser
from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.RATree.Nodes import *
from DDBMS.DB import db

import moz_sql_parser

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
    predicate_dict = moz_sql_parser.parse(dummy_query)[Keywords.WHERE]
    predicate_dict = SQLParser().parsePredicate(predicate_dict) #convert to Columns and Tables
    processed_predicate = SQLQuery.get().newPredicate(predicate_dict) #convert to predicate object
    
    relation_node = RelationNode(table)
    select_seperated = seperateSelect(processed_predicate, relation_node)

    return HorizontalFragNode(name, table, processed_predicate, children=[select_seperated])

#endregion

#region VERTICAL FRAG
@db.execute
def __getVerticalFrags(relation_name):
    #RelationName | AttributeID | FragmentID | FragmentationType | AttributeName | DataType | isKey
    return f"CALL getVerticalFragments('{relation_name}')"

def materialiseVerticalFrag(frag_name, attributes, table):
    cols = []
    for attribute in attributes:
        cols.append(SQLQuery.get().newColumn(name=attribute, table=table))

    relation_node = RelationNode(table)
    project_node = ProjectNode(columns=cols, children=[relation_node])
    return VerticalFragNode(name=frag_name, table=table, columns=cols, children=[project_node])


def joinVerticalFrags(node1, cols_1, node2, cols_2):
    common_cols = list(set(cols_1).intersection(cols_2))
    sub_predicate_dicts = []

    for common_col in common_cols:
        sub_predicate_dict = {PredicateOps.EQ : [common_col, common_col]}
        sub_predicate_dicts.append(sub_predicate_dict)

    processed_predicate = None
    if len(sub_predicate_dicts) == 1:
        processed_predicate = SQLQuery.get().newPredicate(sub_predicate_dicts[0]) 
    else:
        predicate_dict = {PredicateOps.AND : sub_predicate_dicts}
        processed_predicate = SQLQuery.get().newPredicate(predicate_dict)
    
    return JoinNode(join_predicate=processed_predicate, children=[node1, node2])
    
#endregion

#region DERIVED HORIZONTAL FRAG
@db.execute
def __getDerivedHorizontalFrags(relation_name):
    #LeftFragmentID | LeftRelationName | LeftAttributeName | RightFragmentID | RightRelationName | RightAttributeName
    return f"CALL getDerivedHorizontalFragments('{relation_name}')"


def getRightHorizontalFragSelectNode(fragment_details, right_relation, right_relation_node):
    horizontal_frag_details = __getHorizontalFrags(right_relation)
    right_frag_predicate = horizontal_frag_details.loc[horizontal_frag_details['FragmentID'] == fragment_details['RightFragmentID']]['Predicate'].iloc[0]

    dummy_query = f"select * from temp where {right_frag_predicate}".replace('"', "'")
    right_frag_predicate_dict = moz_sql_parser.parse(dummy_query)[Keywords.WHERE]
    right_frag_predicate_dict = SQLParser().parsePredicate(right_frag_predicate_dict)
    right_frag_processed_predicate = SQLQuery.get().newPredicate(right_frag_predicate_dict)
    
    return seperateSelect(right_frag_processed_predicate, right_relation_node)


def materialiseDerivedHorizontalFrag(fragment_details, table : Table):
    right_relation = fragment_details['RightRelationName']
    right_relation_table = SQLQuery.get().newTable(name=right_relation)
    right_relation_node = RelationNode(right_relation_table)
    right_frag_select_node = getRightHorizontalFragSelectNode(fragment_details, right_relation, right_relation_node)

    left_relation_node = RelationNode(table)
    left_col = SQLQuery.get().newColumn(name=fragment_details['LeftAttributeName'],
                                        table=table)
    right_col = SQLQuery.get().newColumn(name=fragment_details['RightAttributeName'],
                                         table=right_relation_table)

    join_predicate_dict = {PredicateOps.EQ : [left_col, right_col]}
    processed_join_predicate = SQLQuery.get().newPredicate(join_predicate_dict)
    join_node = JoinNode(processed_join_predicate, children=[left_relation_node, right_frag_select_node])

    left_relation_cols = SQLQuery.get().filterCols(table=table, aggregation=Aggregation.NONE)
    project_node = ProjectNode(columns=left_relation_cols, children=[join_node])

    return DerivedHorizontalFragNode(table=table,
                                     left_frag_name=fragment_details['LeftFragmentID'],
                                     right_frag_name=fragment_details['RightFragmentID'],
                                     join_predicate=processed_join_predicate,
                                     children=[project_node])

#endregion


def materialiseTable(node : RelationNode):
    table = node.table
    frag_types : DataFrame = __getFragments(table.name)

    if frag_types.iloc[0]['FragmentationType'] == 'H':
        frags = []
        frag_details : DataFrame = __getHorizontalFrags(table.name)
        for idx, frag_detail in frag_details.iterrows():
            frags.append(materialiseHorizontalFrag(frag_detail, table))

        return UnionNode(children=frags)
    
    elif frag_types.iloc[0]['FragmentationType'] == 'V':
        frag_details : DataFrame = __getVerticalFrags(table.name)
        frag_names = frag_details['FragmentID'].unique()
        frags : List[VerticalFragNode]= []

        for frag_name in frag_names:
            frag_detail = frag_details.loc[frag_details['FragmentID'] == frag_name]
            frags.append(materialiseVerticalFrag(frag_name, frag_detail['AttributeName'], table))

        if isinstance(node.parent, ProjectNode):
            required_columns = [set(node.parent.columns).intersection(set(frag.columns)) for frag in frags]
            frag_selection_mask = [True for _ in frags]

            for i, ireq_col in enumerate(required_columns):
                for j in range(i+1, len(required_columns)):
                    jreq_col = required_columns[j]
                    if len(ireq_col) >= len(jreq_col) and len(ireq_col.intersection(jreq_col)) >= len(jreq_col):
                        frag_selection_mask[j] = False
                    elif len(jreq_col) >= len(ireq_col) and len(ireq_col.intersection(jreq_col)) >= len(ireq_col):
                        frag_selection_mask[i] = False

            frags = [frag for i, frag in enumerate(frags) if frag_selection_mask[i]]
            
        cur_node = frags[0]
        cur_cols = cur_node.columns
        for i in range(1, len(frags)):
            new_node = frags[i]
            new_cols = new_node.columns
            cur_node = joinVerticalFrags(cur_node, cur_cols, new_node, new_cols)
            cur_cols = list(set(cur_cols + new_cols))

        return cur_node
    
    elif frag_types.iloc[0]['FragmentationType'] == 'D':
        frags = []
        frag_details : DataFrame = __getDerivedHorizontalFrags(table.name)
        for idx, frag_detail in frag_details.iterrows():
            frags.append(materialiseDerivedHorizontalFrag(frag_detail, table))

        return UnionNode(children=frags)
    
    else:
        return node


def materialiseAllTables(node : Node):
    if isinstance(node, RelationNode):
        new_node = materialiseTable(node)
        parent : Node = node.parent
        if parent is None:
            new_node.makeRoot()
        else:
            parent.replaceChild(node, new_node)
        
        return new_node
    
    for child in node.children:
        materialiseAllTables(child)
    
    return node