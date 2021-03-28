import time

def execute():
    idx = 0

    while True:
        with open("/home/altitude/tmp.txt", "a") as fil:
            fil.write(f"hi {idx}\n")
        
        idx+=1
        time.sleep(5)
    