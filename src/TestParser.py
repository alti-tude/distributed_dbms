from DDBMS.Parser.SQLParser import SQLParser

if __name__ == '__main__':
    query = input()

    parser = SQLParser()
    parsed_query = parser.sql_to_json(query)
    print(parsed_query)