from DDBMS.DB import DBUtils
from Api.User import query
import Config
from .StateManager import StateManager, States

import logging

logger = logging.getLogger(__name__)
state_manager = StateManager()

def prepareMsg(id, query):
    if Config.COMMIT_ABORT_GRACEFULL:
        state_manager.setState(id, States.ABORT)
        logger.info(f"[{id}] abort")
        return False #voteAbort
    
    state_manager.setState(id, States.READY, query)
    logger.info(f"[{id}] ready")

    return True #votCommit

def globalAbortMsg(id):
    state_manager.setState(id, States.ABORT)
    logging.info(f"[{id}] abort")

def globalCommitMsg(id):
    state_manager.setState(id, States.COMMIT)
    logging.info(f"[{id}] commit")
    
    query = state_manager.loadFile(id)["query"]
    DBUtils.directExecuteCommit(query)