#!/usr/bin/python3
"""more listening paths """

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def show():
    return "HBNB"


@app.route("/c/string: name", strict_slashes=False)
def display(name):
    return "C %s" % (name)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
