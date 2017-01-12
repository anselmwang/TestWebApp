"""
Routes and views for the flask application.
"""

from FlaskWebProject1 import app
from flask import request
from flask import jsonify
import flask
import os
import os.path
import Imp


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
    result = digitrec.Predict(sample)
    
    fig = Imp.plt.figure(figsize=(6,4))
    df = Imp.pd.DataFrame({"class" : Imp.np.arange(10), "prob" : result})
    ax = Imp.sns.barplot(x="class", y="prob", data=df)    
    
    figData = Imp.mpld3.fig_to_dict(fig)
   
    return jsonify({"result": result, "figData": Imp.simplejson.dumps(figData, ignore_nan=True)})
    
@app.route('/digitrec/saveInst', methods=['GET', 'POST'])
def digitrec_saveInst():
    inputData = request.get_json()
    target = inputData["target"]
    sample = inputData["sample"]

    with open(os.path.join(digitrec.GetDir(), "data.tsv"), "a") as outF:
        outF.write("%s\t%s\n" % (target, repr(sample)))
    
    return jsonify({"result": digitrec.Predict(sample)})
    