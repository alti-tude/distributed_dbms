from DDBMS.Parser.SQLParser import *
from pprint import PrettyPrinter 
from DDBMS.Execution.BuildTree import buildTree

pp = PrettyPrinter(indent=2, compact=True)

query = "select ScreenID from Screen, Theater where Screen.TheaterID = Theater.TheaterID and Theater.Location = 'Delhi';"
query = "select TheaterID from Screen where TheaterID=1;"

while True:
    
    query = input("> ")

    buildTree(query, "qid")


