from requests.api import request
from requests.exceptions import Timeout
from DDBMS import Routes
from DDBMS.Execution import Site
import logging
import requests
import Config

logger = logging.getLogger(__name__)

def globalAbort(id):
    logger.info("[{id}] abort")

    for site in Site.ALL_SITES:
        url = site.getUrl() + Routes.COMMIT.GLOBAL_ABORT
        requests.get(url, params={"id": id})
    
    logger.info("[{id}] end of transaction")
    return False
    

def twoPC(id, query):
    logger.info("[{id}] begin commit")

    #send prepare
    for site in Site.ALL_SITES:
        url = site.getUrl() + Routes.COMMIT.PREPARE
        try:
            response = requests.get(url, params={"id": id, "query": query}, timeout = Config.COMMIT_TIMEOUT)
            if response.status_code != 200:
                raise ValueError()
        except (ValueError, Timeout):
            return globalAbort(id)

    #send commit
    logger.info("[{id}] commit")
    for site in Site.ALL_SITES:
        url = site.getUrl() + Routes.COMMIT.GLOBAL_COMMIT
        request.get(url, params={"id": id})

    logger.info("[{id}] end of transaction")
    return True
