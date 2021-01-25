from flask import Flask, render_template, jsonify, request
from flask_restful import Api
from routes import initialize_routes
from general_helpers import General_Helpers as GH
from db import db
import util

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/car_search_result", methods=["POST","GET"])
def car_search_result():
    model = str(request.args["model"]).upper()
    zipcode = str(request.args["zipcode"]).upper()
    return render_template("car_search.html", model=model, location=zipcode)

@app.route("/log")
def log():
    log_list = util.getLogFileList()
    return render_template("log.html", loglist=log_list)

@app.route("/log/detail", methods=["POST","GET"])
def log_detail():
    filename = request.form.get("log_name")
    with open("/home/pi/flights-big-data/log/{}".format(filename), "r") as f:
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

@app.route("/db_usage")
def db_usage():
    data = db().db_usage()
    json_data = [{"name": db[0], "usage": db[1]} for db in data]
    return render_template("db_status.html", db_list = json_data)

@app.route("/db_usage/table", methods=['GET','POST'])
def table_usage():
    name = request.form.get("db_name")
    data = db().table_usage(name)
    json_data = [{"name": table[0], "rows": table[1], "usage": table[2]} for table in data]
    return render_template("table_status.html", tables = json_data, name = name)

@app.route("/flight_date_visualization")
def flight_date_dashboard():
    return render_template("date_dashboard.html")

@app.route("/flight_num_retrieval")
def flight_num():
    return render_template("flight_num.html")

@app.route("/airport_detail", methods=["GET"])
def airport_detail():
    name = str(request.args["airport-input"]).upper()
    d = db()
    pop_airline = d.fetchall(db.POP_AIRLINE_BY_AIRPORT_QUERY.format(name))
    airline_list = [{
        "name": "{} ({})".format(i[1], i[0]),
        "count": i[2],
        "url": "https://content.airhex.com/content/logos/airlines_{}_50_15_r.png?proportions=keep".format(i[0])
    } for i in pop_airline]
    dep_delay = d.fetch(db.AVG_DEP_DELAY_QUERY.format(name))
    arr_delay = d.fetch(db.AVG_ARR_DELAY_QUERY.format(name))
    ontime_rate = d.fetchall(db.AIRPORT_DELAY_COUNT_QUERY.format(name, name))
    ontime_arr = d.fetchall(db.AIRPORT_DELAY_ARRIVAL_COUNT_QUERY.format(name, name))
    unique_dest = len(d.fetchall(db.AIRPORT_UNIQUE_DESTINATION_QUERY.format(name)))
    pop_aircraft = d.fetchall(db.POP_AIRCRAFT_BY_AIRPORT_QUERY.format(name))
    ac_list = [{
        "name": "{} ({})".format(i[0], i[2]),
        "count": i[1]
    } for i in pop_aircraft]
    return render_template("airport_detail.html",
                           pop_airlines=airline_list, ontime_arr=ontime_arr, total_dest=unique_dest,
                           ontime_rate = ontime_rate, dep=dep_delay, arr=arr_delay, pop_aircraft=ac_list)

@app.route("/airline_hub")
def airline_hub():
    return render_template("airline_hub.html")

if __name__ == '__main__':
    initialize_routes(api)
    app.run(host='0.0.0.0')
