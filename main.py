import firebase_admin
import json
from re import L
from flask import *
from threading import Timer
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db;
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from operator import itemgetter

class RepeatingTimer(Timer): 
	def run(self):
		while not self.finished.is_set():
			self.function(*self.args, **self.kwargs)
			self.finished.wait(self.interval)

result = None

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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

@app.route("/rr_data", methods=["GET"])
def getRRData():
	return Response(json.dumps(result), mimetype="application/json")

@app.route("/rr", methods=["GET"])
def returnRRPage():
	index_html = open("./rr.html", "r", encoding="utf-8")
	return index_html.read()

def fetchRRData():
	global result
	user_refs = db.collection(u'user')
	docs = user_refs.stream()
	result = []
	for data in docs:
		dict = data.to_dict()

		if("CodeForcesRating" not in dict):
			dict["CodeForcesRating"] = 0

		dict["user_id"] = data.id
		result.append(dict)
	result.sort(key = itemgetter('CodeForcesRating'), reverse=True)

if __name__ == "__main__":

	fetchRRData()

	scheduler = BackgroundScheduler(daemon=True)
	scheduler.add_job(func=fetchRRData, trigger="interval", minutes=30)
	scheduler.start()

	app.run(threaded=True, host="0.0.0.0", port=80)
