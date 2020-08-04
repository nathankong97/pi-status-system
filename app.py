from flask import Flask, render_template, jsonify
import os, json
from flask_restful import Api
from routes import initialize_routes

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

@app.route("/")
def new_index():
    return render_template("index.html")

@app.route("/test")
def status():
    return render_template('test.html')

if __name__ == '__main__':
    initialize_routes(api)
    app.run(host='0.0.0.0')
    #app.run()
