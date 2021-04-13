from DDBMS.CommitProtocol.Worker import globalAbortMsg, globalCommitMsg, prepareMsg 
from flask import Blueprint, request, Response
import os
import signal


bp = Blueprint(name="commit", import_name = __name__, url_prefix="/commit")

@bp.route("/prepare", methods=["GET", "PUT"])
def prepare():
    id = request.args["id"]
    query = request.args["query"]

    if prepareMsg(id, query):
        return Response("vote-commit", status=200)
    
    return Response("vote-abort", status=400)


@bp.route("/global_abort", methods=["GET", "PUT"])
def globalAbort():
    id = request.args["id"]

    globalAbortMsg(id)

    return Response(status=200)

@bp.route("/global_commit", methods=["GET", "PUT"])
def globalCommit():
    id = request.args["id"]

    pid = os.fork()
    if pid == 0:
        globalCommitMsg(id)
        os.kill(os.getpid(), signal.SIGKILL)

    return Response(status=200)


