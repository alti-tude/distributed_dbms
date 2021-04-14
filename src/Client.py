import requests
import time

import argparse
import pandas as pd

retry_delay = 1
parser = argparse.ArgumentParser()
parser.add_argument("--retry-delay", type=int, help="time for result retry delay (seconds)", dest='retry_delay')
parser.add_argument("--timeout", type=int, help="time till client times out", dest='client_timeout')
args = parser.parse_args()

retry_delay = args.retry_delay
client_timeout = args.client_timeout

query_url = f"http://10.3.5.215:12345/user/query"
update_url = f"http://10.3.5.215:12345/user/update"

while True:
    query = input("> ")

    def getData(query):
        response = requests.get(query_url, params={"query": query})
        print(response)
        response = response.json()
        
        result_url = response["result_url"]
        id = response["id"]

        print(result_url)
        response = requests.get(result_url, params={"id": id})
        retry_cnt = 0
        while response.status_code != 200 and (retry_cnt*retry_delay) <= client_timeout:
            response = requests.get(result_url, params={"id": id})
            time.sleep(retry_delay)
            retry_cnt += 1
            
        return pd.DataFrame(response.json())

    pd.set_option('display.expand_frame_repr', False)
    if "update" in query.lower().strip()[:6]:
        response = requests.get(update_url, params={"query": query})
        print(response)
    else:
        print(getData(query))