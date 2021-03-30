from Config import DEBUG
from DDBMS import BasePrimitive
from DDBMS.DB import db

@db.execute
def getSiteData(site_id):
    return f"select * from `Site` where SiteID='{site_id}'"

class Site(BasePrimitive):
    ALL_SITES = []
    CUR_SITE = None

    def __init__(self, name, ip=None, port=None):
        self.name = name

        if ip == None or port == None:
            site_data = getSiteData(self.name)
            if DEBUG:
                print(site_data)

            self.ip = ip if ip is not None else str(site_data.iloc[0]["IP"])
            self.port = port if port is not None else str(site_data.iloc[0]["Port"])
        else:
            self.ip = ip
            self.port = port

        if self not in Site.ALL_SITES:
            Site.ALL_SITES.append(self)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Site):
            return self.name == o.name
        else:
            return super().__eq__(o)

    def getUrl(self):
        return f"http://{self.ip}:{self.port}"

    def to_dict(self):
        return {
            "name": self.name,
            "ip": self.ip,
            "port": self.port
        }