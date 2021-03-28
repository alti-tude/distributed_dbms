import requests
import time

import argparse

from Config import SITE_CONFIG

retry_delay = 1
parser = argparse.ArgumentParser()
parser.add_argument("--retry-delay", type=int, help="time for result retry delay (seconds)", dest=retry_delay)
query_url = f"http://{SITE_CONFIG.IP[0]}:{SITE_CONFIG.IP[1]}/user/query"

while True:
    query = input("> ")

    response = requests.get(query_url, params={"query": query})
    response = response.json()
    
    result_url = response["result_url"]
    id = response["id"]

    response = requests.get(result_url, params={"id": id})
    while response.status_code == 404:
        response = requests.get(result_url, params={"id": id})
        time.sleep(retry_delay)
        
    print(response.text)


