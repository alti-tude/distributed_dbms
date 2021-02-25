# TODO we assume that attribute relation mapping is on top of the csv, need to handle if not

import csv
from DDBMS.DB import db

@db.execute_commit
def deleteTable(table):
    return "DELETE FROM " + table + ";"

@db.execute_commit
def insertIntoTable(table, values):
    return "INSERT INTO " + table + " VALUES " + str(values) + ';'

@db.execute_commit
def insertIntoAttribute(values):
    return "INSERT INTO Attribute (RelationName, AttributeName, DataType, isKey) VALUES " + str(values) + ';'

@db.execute_commit
def insertIntoVerticalFragment(frag, relation, attrs):
    attrs_str = "("
    for attr in attrs:
        if attrs_str != "(":
            attrs_str += " OR "
        attrs_str += "AttributeName = '" + attr + "'"
    attrs_str += ")"
    return "INSERT INTO VerticalFragment SELECT '" + frag + "', AttributeID FROM Attribute WHERE RelationName = '" + relation + "' AND " + attrs_str 


@db.execute_commit
def insertIntoDerivedHorizontalFragment(l_relation, l_attr, l_frag, r_relation, r_attr, r_frag):
    return "CALL insertDerivedHorizontalFragment('" + l_relation + "', '" + l_attr + "', '" + l_frag + "', '" + r_relation + "', '" + r_attr + "', '" + r_frag + "')"

def clearAllTables():
    tables = ["LocalMapping", "VerticalFragment", "HorizontalFragment", "DerivedHorizontalFragment", "Site", "Fragment", "Attribute"]
    for table in tables:
        deleteTable(table)


def readSysCatalogCSV(input_file):
    read_frag_type = False
    read_frag_site = False
    read_attr = False

    horizontal_frag_map = {}
    derived_insert_vals = []

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 0 or row[0] == '':
                read_frag_type = False
                read_frag_site = False
                read_attr = False

            if read_frag_type:
                frag_type = row[2][0]
                values = (row[1], frag_type, row[0])
                insertIntoTable("Fragment", values)

                if frag_type == 'H':
                    predicate = row[3].strip('[]')
                    values = (row[1], predicate)
                    insertIntoTable("HorizontalFragment", values)
                    horizontal_frag_map[row[1]] = row[0]
                elif frag_type == 'V':
                    attrs = [x.strip(' ') for x in row[3].strip().strip('[]').split(',')]
                    insertIntoVerticalFragment(row[1], row[0], attrs)
                else:
                    attrs = [x.strip(' ') for x in row[3].strip().strip('[]').split(',')]
                    derived_insert_vals.append([row[0], attrs[0], row[1], attrs[1], attrs[2]])                
            
            if read_attr:
                # TODO change row[1], row[0] according to how it will actually be
                values = (row[1], row[0], "INT", 1)
                insertIntoAttribute(values)

            if row[0:4] == ['Relation', 'Fragment', 'FragmentType', 'Details']:
                read_frag_type = True
            if row[0:2]== ['Attribute', 'Relation']: #TODO change according to how it will actually be
                read_attr = True

    for val in derived_insert_vals:
        right_frag = val[4]
        right_relation = horizontal_frag_map[right_frag]
        insertIntoDerivedHorizontalFragment(val[0], val[1], val[2], right_relation, val[3], val[4])

if __name__ == '__main__':
    clearAllTables()

    # TODO change path
    readSysCatalogCSV('../../trial.csv')