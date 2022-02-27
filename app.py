from flask import Flask, render_template
from db import connect_to_database, select_last_test, select_sites

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index_page():
    site_status = get_status()
    return render_template("index.html", site_status=site_status)


@app.route('/tech', methods=["GET"])
def tech_page():
    return render_template("tech.html")


@app.route('/about', methods=["GET"])
def about_page():
    return render_template("about.html")


@app.route('/authors', methods=["GET"])
def authors_page():
    return render_template("authors.html")


def get_status():
    site_status = {}
    sites = select_sites(connect_to_database())
    for site in sites:
        site_report = list(select_last_test(connect_to_database(), site[0]))
        site_status[site[0]] = {'name': site_report[1],
                             'response_code': str(site_report[2]),
                             'score': site_report[3],
                             'speed_score': site_report[4],
                             'tti': site_report[5]}

    return site_status


if __name__ == '__main__':
    app.run()
