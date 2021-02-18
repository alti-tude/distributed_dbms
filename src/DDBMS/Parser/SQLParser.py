import moz_sql_parser
from DDBMS.DB import db
from DDBMS.Parser.SQLQuery import *

class SQLParser:
    def __init__(self):
        self.formatted_query = SQLQuery()
        self.schema = self.getApplicationSchema()

    def reset(self):
        self.formatted_query.reset()

    @db.execute
    def getApplicationSchema(self):
        return "SELECT * FROM Attribute;"

    def parse(self, original_query):
        query = original_query.replace('"', "'")
        query = moz_sql_parser.parse(query)

        self.addFromTables(query)
        self.addSelectColumns(query)
        self.addGroupbyColumns(query)

        print(query)
        print(self.formatted_query.tables)
        print(self.formatted_query.select)
        print(self.formatted_query.groupby)

        self.reset()
        return self.formatted_query


    def addFromTables(self, query):
        from_query = query['from']
        from_tables = [from_query] if not isinstance(from_query, list) else from_query

        for table in from_tables:
            cur_table = None
            if isinstance(table, dict):
                cur_table = Table(table['value'], table['name'])
            else:
                cur_table = Table(table)
            self.formatted_query.addFrom(cur_table)


    def addAllSelectColumns(self, aggr):
        for table in self.formatted_query.tables:
            for _, row in self.schema.iterrows():
                relation = row['RelationName']
                attr = row['AttributeName']

                if table.name == relation:
                    self.formatted_query.addSelectColumn(attr, table, aggregation=aggr)


    def mapColToTable(self, col_name, table_alias=None):
        for table in self.formatted_query.tables:
            if table_alias is not None and table_alias != table.alias:
                continue

            for _, row in self.schema.iterrows():
                relation = row['RelationName']
                attr = row['AttributeName']  

                if table.name == relation and col_name == attr:
                    return table

    
    def parseColumn(self, col_name):
        col_details = col_name.split('.')

        if len(col_details) == 1:
            return self.mapColToTable(col_details[0]), col_details[0]
        else:
            return self.mapColToTable(col_details[1], col_details[0]), col_details[1] 


    def addSelectColumns(self, query):
        select_query = query['select']
        select_cols = [select_query] if not isinstance(select_query, list) else select_query

        for col in select_cols:
            select_all_present = True if col == '*' else False
            select_all_aggr = Aggregation.NONE

            '''
            TODO Need to think what to do if it is count(*)
            Do we replace with all columns? What about aliasing being there?
            e.g. select count(*) as total
            '''
            if isinstance(col, dict) and isinstance(col['value'], dict):
                col_aggr = next(iter(col['value']))
                if col['value'][col_aggr] == '*':
                    select_all_present = True
                    select_all_aggr = col_aggr
            

            if select_all_present:
                self.addAllSelectColumns(select_all_aggr)
            else:
                col_name = col['value']
                col_aggr = Aggregation.NONE
                col_alias = None

                if isinstance(col['value'], dict):
                    col_aggr = next(iter(attr['value']))
                    col_name = col['value'][col_aggr]
                if 'name' in col:
                    col_alias = col['name']

                col_table, col_name = self.parseColumn(col_name)
                self.formatted_query.addSelectColumn(col_name, col_table, col_alias, col_aggr)


    def addGroupbyColumns(self, query):
        groupby_query = query['groupby']
        groupby_cols = [groupby_query] if not isinstance(groupby_query, list) else groupby_query

        for col in groupby_cols:
            col_table, col_name = self.parseColumn(col['value'])
            self.formatted_query.addGroupbyColumn(col_name, col_table)