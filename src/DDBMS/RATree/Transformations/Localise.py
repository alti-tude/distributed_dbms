from DDBMS.DB import db
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
def __getHorizontalFrags(relation_name):
    return f"CALL getHorizontalFragments({relation_name})"

def materialiseHorizontalFrag(fragment_details):
    #FragmentID | FragmentationType | RelationName | Predicate
    fragment_details['']