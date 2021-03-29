import mysql.connector
import pandas as pd
import contextlib

class DB:
    def __init__(self, config):
        self.config = config
        self._return_strings = False

    @contextlib.contextmanager
    def returnStrings(self):
        self._return_strings = True
        yield

        self._return_strings = False

    def execute(self, query_function):
        def wrapper(*args, **kwargs):
            conn = mysql.connector.connect(**self.config)
            cur = conn.cursor()
            
            query = query_function(*args, **kwargs)
            if self._return_strings: return query

            assert(isinstance(query,str))
            cur.execute(query)

            result = [item for item in cur]
            column_names = [item for item in cur.column_names]

            cur.close()
            conn.close()

            return pd.DataFrame(result, columns=column_names)
        
        return wrapper
    
    def execute_commit(self, query_function):
        def wrapper(*args, **kwargs):
            conn = mysql.connector.connect(**self.config)
            cur = conn.cursor()
            
            query = query_function(*args, **kwargs)
            if self._return_strings: return query
            
            assert(isinstance(query,str))
            cur.execute(query)

            result = [item for item in cur]
            column_names = [item for item in cur.column_names]

            conn.commit()
            cur.close()
            conn.close()

            return pd.DataFrame(result, columns=column_names)
        
        return wrapper
