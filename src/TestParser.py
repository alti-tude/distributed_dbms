from DDBMS.Parser.Exceptions.SQLParserException import SQLParserException
from DDBMS.Parser.SQLParser import SQLParser

if __name__ == '__main__':
    query = input()

    parser = SQLParser()
    try:
        parsed_query = parser.sql_parse(query)
        print(parsed_query)
    except SQLParserException as e:
        print(e)
        