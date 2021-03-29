from DDBMS import BasePrimitive
from DDBMS.DB import db

@db.execute
def __getSiteData(site_id):
    return f"select * from `Site` where SiteID='{site_id}'"

class Site(BasePrimitive):
    def __init__(self, name, ip=None, port=None):
        self.name = name

        if ip == None or port == None:
            site_data = __getSiteData(self.name)
            self.ip = ip if ip is not None else str(site_data["IP"])
            self.port = port if port is not None else str(site_data["Port"])
        else:
            self.ip = ip
            self.port = port

    def getUrl(self):
        return f"http://{self.ip}:{self.port}"

    def to_dict(self):
        return {
            "name": self.name,
            "ip": self.ip,
            "port": self.port
        }