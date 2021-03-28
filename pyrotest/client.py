import Pyro4

proxy = Pyro4.Proxy("PYRONAME:test@10.3.5.215:12345")
print(proxy.run("somthing"))