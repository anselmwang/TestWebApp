from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/add")
def add():
    a = int(request.args.get("a", '0'))
    b = int(request.args.get("b", '0'))
    return str(a+b)

@app.route("/")
def index():
    return "hello, yw"

if __name__ == "__main__":
    app.run()