from DDBMS.Parser.SQLParser import SQLParser

if __name__ == '__main__':
    query = input()

    parser = SQLParser()
    parsed_query = parser.sql_parse(query)
    print(parsed_query)