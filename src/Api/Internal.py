from DDBMS.Execution import buildTree
from DDBMS.RATree.RATreeBuilder import RATreeBuilder
from DDBMS.Parser import SQLParser
from DDBMS.Parser.SQLQuery import SQLQuery
from DDBMS import execute
from DDBMS.Execution import DataTransfer
from DDBMS.CommitProtocol import Master
from Config import DEBUG

from flask import request, Response, Blueprint

import traceback
import os, signal

bp = Blueprint(name="internal", import_name = __name__, url_prefix="/internal")

@bp.route("/query", methods=["GET", "POST"])
def internalQuery():
    query = request.args["query"]
    id = request.args["id"]

    if DEBUG:
        print(query, id)

    try:
        root = buildTree(query, id)

        pid = os.fork()
        if pid == 0:
            execute(root, id)
            os.kill(os.getpid(), signal.SIGKILL)
            # exit(0)

    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return Response(str(e), status=500)

    return {
        "ip": root.site.ip, 
        "port": root.site.port,
        "operation_id": root.operation_id
    }

@bp.route("/put", methods=["GET", "POST"])
def put():
    payload = request.json
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(payload["query_id"], payload["operation_id"])
    DataTransfer.put(**payload)
    
    return Response(status=200)


