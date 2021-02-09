import mysql.connector
import pandas as pd

class DB:
    def __init__(self, *, config):
        self.config = config

    def execute(self, query_function):
        def wrapper(*args, **kwargs):
            conn = mysql.connector.connect(**self.config)
            cur = conn.cursor()
            
            query = query_function(*args, **kwargs)
            assert(isinstance(query,str))
            cur.execute(query)

            result = [item for item in cur]
            column_names = [item for item in cur.column_names]

            cur.close()
            conn.close()

            return pd.DataFrame(result, columns=column_names)
        
        return wrapper
