LOCAL_DB_CONFIG = {
    "user": "ddbms2",
    "password": "ddbms",
    "host": "localhost",
    "database": "ddbms",
}


SERVER_DB_CONFIG = {
    "user": "Samosa",
    "password": "Samose",
    "host": "localhost",
    "database": "Samosa",
}

ConfigToUse = LOCAL_DB_CONFIG
GET_RETRY_DELAY = 0.1 #in seconds
SELECTIVITY_FACTOR = 0.3

DEBUG = True
LOCAL_SERVERS = True

COMMIT_ABORT_GRACEFULL = True
COMMIT_ABORT = False

COMMIT_STATE_FOLDER = "./"
COMMIT_TIMEOUT = 4