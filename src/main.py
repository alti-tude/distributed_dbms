from DDBMS.Execution import Site
from DDBMS.Execution.DataTransfer import get, send
from numpy import insert
from DDBMS.Parser.SQLQuery.Column import Column
from DDBMS.Parser.SQLQuery.Table import Table
from DDBMS.DB import db
from DDBMS.DB.DBUtils import *

columns = [
    Column("MovieId", alias="id", table=Table("Movie")),
    Column("Location", alias="loc", table=Table("Theater")),
    Column("Price", table=Table("Show"))
]

col_names = ["id", "loc", "price"]

data = {
    "id": [1,2],
    "loc": ["loc1", "loc2"],
    "price": [10.0201, 11]
}

data = pd.DataFrame(data)

send(Site("hyderabad", "localhost", 12345),"quid", "oid", data, columns)
print(get("quid", "oid"))
