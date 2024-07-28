#!/usr/bin/python3
"""This Script listens to port 5000 on 0.0.0.0"""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    return "Hello HBNB"


@app.route("/hbnb", strict_slashes=False)
def show():
    return "HBNB"


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
