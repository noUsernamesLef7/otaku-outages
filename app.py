from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index_page():
    return render_template("index.html")

@app.route('/tech', methods=["GET"])
def tech_page():
    return render_template("tech.html")

@app.route('/about', methods=["GET"])
def about_page():
    return render_template("about.html")

@app.route('/authors', methods=["GET"])
def authors_page():
    return render_template("authors.html")


if __name__ == '__main__':
    app.run()
