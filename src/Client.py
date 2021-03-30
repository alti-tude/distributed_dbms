import requests
import time

import argparse

from Config import SITE_CONFIG

retry_delay = 1
parser = argparse.ArgumentParser()
parser.add_argument("--retry-delay", type=int, help="time for result retry delay (seconds)", dest='retry_delay')
args = parser.parse_args()

retry_delay = args.retry_delay

query_url = f"http://localhost:12345/user/query"

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
        while response.status_code == 404:
            response = requests.get(result_url, params={"id": id})
            time.sleep(retry_delay)
            
        # print(response.text)

    getData(query)


