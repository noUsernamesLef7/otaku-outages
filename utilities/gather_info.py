import urllib.request
import json
import cloudscraper
from .. import db


def populate_db():
    # open DB connection
    conn = db.connect_to_database()
    # prep cloudscraper
    scraper = cloudscraper.create_scraper()

    # pull list of names/urls from the DB
    # key = name, value = url
    website_list = db.select_sites(conn)

    for site in website_list:
        # check if site is crunchyroll
        if site.lower() == "crunchyroll":
            # use cloudscraper to bypass Crunchyroll lmao gottem ggs no re
            is_up = scraper.get("https://www.crunchyroll.com").status_code
            # insert into DB, adding null values for the ones we can't obtain
            db.insert_test(conn, site, is_up, None, None, None)
        # use this for every other site
        else:
            # dynamically build URL to request from using Google PageSpeed Insight
            url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" \
                  + website_list.get(site) + \
                  "&strategy=desktop&key=AIzaSyCQONQHpQ3hIcxf1G-rPtM011kt5qefQRU"

            # make request and create object for the json data
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())

            # assign DB variables
            is_up = response.getcode()
            overall_score = data["lighthouseResult"]["categories"]["performance"]["score"]
            speed_index_score = data["lighthouseResult"]["audits"]["speed-index"]["score"]
            time_interactive_score = data["lighthouseResult"]["audits"]["interactive"]["score"]

            # insert into DB
            db.insert_test(conn, site, is_up, overall_score, speed_index_score,
                           time_interactive_score)
    conn.close()
    return
