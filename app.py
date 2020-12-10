from flask import Flask, render_template, jsonify, request
import os, json
from flask_restful import Api
from routes import initialize_routes
from general_helpers import General_Helpers as GH
import util

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log")
def log():
    log_list = util.getLogFileList()
    return render_template("log.html", loglist=log_list)

@app.route("/log/detail", methods=["POST","GET"])
def log_detail():
    filename = request.form.get("log_name")
    with open("/home/pi/flights_big_data/log/{}".format(filename), "r") as f:
        content = f.read()
    return render_template("log_detail.html", name = filename, text = content)

@app.route("/search")
def flightSearch():
    return render_template("search.html")

@app.route("/search/dashboard", methods=['GET','POST'])
def dashboard():
    iata = str(request.args["airport"]).upper()
    countryCode = GH.getCountryCodeByIATA(iata)
    return render_template("dashboard.html", countryCode = countryCode)


if __name__ == '__main__':
    initialize_routes(api)
    app.run(host='0.0.0.0')
