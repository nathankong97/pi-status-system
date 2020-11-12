from flask import Flask, render_template, jsonify
import os, json
from flask_restful import Api
from routes import initialize_routes

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log")
def log():
    return render_template("log.html")

@app.route("/search")
def flightSearch():
    return render_template("search.html")



if __name__ == '__main__':
    initialize_routes(api)
    app.run(host='0.0.0.0')
