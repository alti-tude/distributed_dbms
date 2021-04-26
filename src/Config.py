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

ConfigToUse = SERVER_DB_CONFIG
GET_RETRY_DELAY = 0.3 #in seconds
SELECTIVITY_FACTOR = 0.3

DEBUG = True
LOCAL_SERVERS = False

COMMIT_ABORT_GRACEFULL = False

COMMIT_STATE_FOLDER = "./states"
COMMIT_TIMEOUT = 4
