"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject1 import app
from flask import request

@app.route('/')
def home():
    """Renders the home page."""
    return app.send_static_file("index.html")
    #return "abcdef"

@app.route('/add')
def add():
    return str(int(request.args.get('a', '0')) +int(request.args.get('b', '0')))