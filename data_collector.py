from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from app import app
@app.route("/low/data/<num_attributes>")
def collect_data_low(num_attributes):
