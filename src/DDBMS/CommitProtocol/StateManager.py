from collections import defaultdict
import os
import json

import Config

class States:
    INIT = "INIT",
    READY = "READY",
    COMMIT = "COMMIT",
    ABORT = "ABORT"

class StateManager:
    def __init__(self) -> None:
        self.state_folder = Config.COMMIT_STATE_FOLDER
    
    def filename(self, id):
        return os.path.join(self.state_folder, id)

    def loadFile(self, id):
        if not os.path.isfile(self.filename(id)):
            return {}

        with open(self.filename(id), "r") as fil:
            return json.load(fil)

    def saveFile(self, id, data):
        with open(self.filename(id), "w") as fil:
            return json.dump(data, fil)

    def setState(self, id, state, query=None):
        cur_data = self.loadFile(id)

        cur_data["state"] = state
        if query is not None:
            cur_data["query"] = query

        self.saveFile(id, cur_data)

    def getState(self, id):
        return self.loadFile(id)["state"]
