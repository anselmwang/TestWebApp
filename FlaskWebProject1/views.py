"""
Routes and views for the flask application.
"""

from FlaskWebProject1 import app
from flask import request
from flask import jsonify
import flask

@app.route("/app/<path:filename>")
def send_app(filename):
    # the root directory is the python file (which create Flask instance)'s directory
    return flask.send_file(flask.safe_join("app", filename))

@app.route("/static/<path:filename>")
def send_static(filename):
    # the root directory is the python file (which create Flask instance)'s directory
    return flask.send_file(flask.safe_join("static", filename))


@app.route('/add/add')
def add():
    return str(int(request.args.get('a', '0')) +int(request.args.get('b', '0')))

import digitrec
@app.route('/digitrec/predict', methods=['GET', 'POST'])
def digitrec_predict():
    sample = request.get_json()
    return jsonify({"result": digitrec.Predict(sample)})