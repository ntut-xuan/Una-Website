from re import L
from flask import *

app = Flask(__name__)

@app.route("/static/<path:path>")
def returnStaticFile(path):
    return send_from_directory('static', path)

@app.route("/", methods=["GET"])
def returnIndexPage():
    index_html = open("./index.html", "r", encoding="utf-8")
    return index_html.read()

@app.route("/help", methods=["GET"])
def returnHelpPage():
    index_html = open("./help.html", "r", encoding="utf-8")
    return index_html.read()

@app.errorhandler(404)
def return404Page(e):
    index_html = open("./404.html", "r", encoding="utf-8")
    return index_html.read(), 404

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)