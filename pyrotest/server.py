import Pyro4
import numpy as np

@Pyro4.expose
class test:
    def __init__(self):
        pass

    def run(self, s):
        return np.array(s)


daemon = Pyro4.Daemon(host='10.3.5.215', port=12346)
uri = daemon.register(test)
Pyro4.locateNS(port=12345).register("test", uri)

print("started")
daemon.requestLoop()

