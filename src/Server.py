from Api import app
from Config import SITE_CONFIG

if __name__ == '__main__':
    print(SITE_CONFIG.IP)
    print(app.url_map)
    app.run(debug=True, host = SITE_CONFIG.IP[0], port=SITE_CONFIG.IP[1])
