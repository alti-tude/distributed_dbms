from DDBMS.Execution import Site
from DDBMS.Execution.DataTransfer import getTempTableName
from flask import request, Response, Blueprint
import requests

import uuid
import random

from Config import DEBUG

bp = Blueprint(name="user", import_name = __name__, url_prefix="/user")

@bp.route("/query", methods=["GET", "POST"])
def query():
    id = str(uuid.uuid4())
    if "query" not in request.args:
        return Response(status=400)
    
    query = request.args["query"]
    
    #TODO replace with new site object instead of config hardcode
    for site in Site.ALL_SITES:
        forward_url = f"{site.getUrl()}/internal/query"
        response = requests.get(forward_url, params={"query": query, "id": id})
        if response.status_code != 200:
            return Response(response.text, response.status_code, response.headers.items())

    response = response.json()
    output_table_name = getTempTableName(id, response["operation_id"])
    return {
        "id": id, 
        "result_url": f"http://{response['ip']}:{response['port']}/user/result?id={output_table_name}"
    }

@bp.route("/result", methods=["GET", "POST"])
def result():
    id = request.args["id"]

    if DEBUG:
        print(id)
    
    if random.random() > 0.5:
        return Response(status=404)
    
    return Response("final", status=200)
