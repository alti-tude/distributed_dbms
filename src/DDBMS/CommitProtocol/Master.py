from requests.api import request
from requests.exceptions import Timeout
from DDBMS import Routes
from DDBMS.Execution import Site
import logging
import requests
import Config

logger = logging.getLogger(__name__)

def globalAbort(id):
    logger.info(f"[{id}] abort")

    for site in Site.ALL_SITES:
        url = site.getUrl() + Routes.COMMIT.GLOBAL_ABORT
        try:
            requests.get(url, params={"id": id}, timeout = Config.COMMIT_TIMEOUT)
        except:
            continue

    logger.info(f"[{id}] end of transaction")
    return False
    

def twoPC(id, query):
    print("Beginning 2PC")
    logger.info(f"[{id}] begin commit")

    #send prepare
    for site in Site.ALL_SITES:
        url = site.getUrl() + Routes.COMMIT.PREPARE
        print(url)
        try:
            response = requests.get(url, params={"id": id, "query": query}, timeout = Config.COMMIT_TIMEOUT)
            if response.status_code != 200:
                raise ValueError()
        except:
            return globalAbort(id)

    #send commit
    logger.info(f"[{id}] commit")
    for site in Site.ALL_SITES:
        url = site.getUrl() + Routes.COMMIT.GLOBAL_COMMIT
        requests.get(url, params={"id": id})

    logger.info(f"[{id}] end of transaction")
    return True
