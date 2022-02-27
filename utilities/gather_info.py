import urllib.request
import json
import cloudscraper
from .. import db


def everything_else_info():
    conn = db.connect_to_database()
    scraper = cloudscraper.create_scraper()

    # key = name, value = url
    website_list = db.select_sites(conn)

    for site in website_list:
        if site.lower() == "crunchyroll":
            is_up = scraper.get("https://www.crunchyroll.com").status_code
            db.insert_test(conn, site, is_up, None, None, None)
        else:
            url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" \
                  + website_list.get(site) + \
                  "&strategy=desktop&key=AIzaSyCQONQHpQ3hIcxf1G-rPtM011kt5qefQRU"

            # create object for the json data
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())

            is_up = response.getcode()
            overall_score = data["lighthouseResult"]["categories"]["performance"]["score"]
            speed_index_score = data["lighthouseResult"]["audits"]["speed-index"]["score"]
            time_interactive_score = data["lighthouseResult"]["audits"]["interactive"]["score"]

            db.insert_test(conn, site, is_up, overall_score, speed_index_score,
                           time_interactive_score)
    conn.close()
    return
