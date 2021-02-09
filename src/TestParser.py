from DDBMS.Parser.SQLParser import *

if __name__ == '__main__':
    query = input()

    parsed_query = parse_sql(query)
    print(parsed_query)

    verify(parsed_query)
        