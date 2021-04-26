import os
import logging
import Config

logging.basicConfig(filename=os.path.join(Config.COMMIT_STATE_FOLDER, "commit_protocol.log"),
                            filemode='a',
                            level=logging.info)

logger = logging.getLogger(__name__)
