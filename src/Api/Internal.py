import os
from DDBMS.RATree.RATreeBuilder import RATreeBuilder
from DDBMS.RATree.Optimise import optimise
from DDBMS.Parser import SQLParser
from DDBMS.Parser.SQLQuery import SQLQuery

from . import app
from Config import DEBUG, SITE_CONFIG
from DDBMS import execute

from flask import request, Response, Blueprint

import daemon

bp = Blueprint(name="internal", import_name = __name__, url_prefix="/internal")

@bp.route("/query", methods=["GET", "POST"])
def internalQuery():
    query = request.args["query"]
    id = request.args["id"]

    if DEBUG:
        print(query, id)

    try:
        SQLQuery.reset()
        parser = SQLParser()
        parser.parse(query)

        root = optimise()
        pid = os.fork()
        if pid == 0:
            with daemon.DaemonContext():
                execute()

    except Exception as e:
        return Response(str(e), status=500)

    return {
        "ip": SITE_CONFIG.IP[0], 
        "port": SITE_CONFIG.IP[1]
    }
    