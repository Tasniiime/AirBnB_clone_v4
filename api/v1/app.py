#!/usr/bin/python3
"""
Flask application setup
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the app views blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Teardown context to close the storage
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handle 404 errors with a JSON response
    :return: JSON response with error message
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    # Run the application using environment variables for host and port
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
