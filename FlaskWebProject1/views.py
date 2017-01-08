"""
Routes and views for the flask application.
"""

from FlaskWebProject1 import app
from flask import request
from flask import jsonify
import digitrecCore

@app.route('/')
def home():
    """Renders the home page."""
    return app.send_static_file("index.html")


@app.route('/add')
def add():
    return str(int(request.args.get('a', '0')) +int(request.args.get('b', '0')))

@app.route("/digitrec")
def digitrec():
    """Renders the home page."""
    return app.send_static_file("digitrec.html")
    

@app.route('/digitrec_predict', methods=['GET', 'POST'])
def digitrec_predict():
    sample = request.get_json()
    return jsonify({"result": digitrecCore.Predict(sample)})
    

