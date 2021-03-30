from .BasePrimitive import BasePrimitive
from DDBMS.Execution import Site
import Config
import os

if Config.LOCAL_SERVERS:
    h = Site("Hyderabad", "localhost", 12345)
    d = Site("Delhi", "localhost", 12347)
    m = Site("Mumbai", "localhost", 12346)
else:
    h = Site("Hyderabad")
    d = Site("Delhi")
    m = Site("Mumbai")

print(os.environ["SITE"])
if os.environ["SITE"] == "Hyderabad":
    Site.CUR_SITE = h

if os.environ["SITE"] == "Delhi":
    Site.CUR_SITE = d

if os.environ["SITE"] == "Mumbai":
    Site.CUR_SITE = m


from .Execution import execute