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
DEBUG = True

class HYDERABAD_CONFIG:
    IP = ("localhost", 12345)
    OTHER_SITES = [
        ("localhost", 12346),
        ("localhost", 12347)
    ]

class MUMBAI_CONFIG:
    IP = ("localhost", 12346)
    OTHER_SITES = [
        ("localhost", 12345),
        ("localhost", 12347)
    ]
    
class DELHI_CONFIG:
    IP = ("localhost", 12347)
    OTHER_SITES = [
        ("localhost", 12345),
        ("localhost", 12346)
    ]
    
SITE_CONFIG = HYDERABAD_CONFIG

def getEnvConfig():
    import os

    global SITE_CONFIG    
    if "SITE" in os.environ:
        site = os.environ["SITE"]
        if site == "hyderabad":
            SITE_CONFIG = HYDERABAD_CONFIG
        if site == "delhi":
            SITE_CONFIG = DELHI_CONFIG
        if site == "mumbai":
            SITE_CONFIG = MUMBAI_CONFIG

getEnvConfig()