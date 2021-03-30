from Api import app
from DDBMS.Execution import Site

if __name__ == '__main__':
    print(Site.CUR_SITE)
    print(app.url_map)
    app.run(debug=True, host = Site.CUR_SITE.ip, port=Site.CUR_SITE.port)
