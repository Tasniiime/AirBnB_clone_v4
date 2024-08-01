#!/usr/bin/python3
"""This script starts the  flask web"""
from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    """method to display string"""
    return "Hello HBNB"


@app.route("/hbnb")
def display():
    """method to  display HBNB"""
    return "HBNB"


if __name__ == "__main__":
    app.run()
