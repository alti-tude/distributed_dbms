from DDBMS.Execution import buildTree
import os
from DDBMS.RATree.RATreeBuilder import RATreeBuilder
from DDBMS.Parser import SQLParser
from DDBMS.Parser.SQLQuery import SQLQuery

from Config import DEBUG, SITE_CONFIG
from DDBMS import RATree, execute
from DDBMS.Execution import DataTransfer

from flask import request, Response, Blueprint

import daemon
import traceback

bp = Blueprint(name="internal", import_name = __name__, url_prefix="/internal")

@bp.route("/query", methods=["GET", "POST"])
def internalQuery():
    query = request.args["query"]
    id = request.args["id"]

    if DEBUG:
        print(query, id)

    try:
        root = buildTree(query)

        pid = os.fork()
        if pid == 0:
            with daemon.DaemonContext():
                execute()

    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return Response(str(e), status=500)

    return {
        "ip": root.site.ip, 
        "port": root.site.port
    }

@bp.route("/put", methods=["GET", "POST"])
def put():
    payload = request.json
    
    if DEBUG:
        print(payload)
    
    DataTransfer.put(**payload)

    return Response(status=200)