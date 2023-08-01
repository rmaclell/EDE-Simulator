import random
import sqlite3
from flask import request, url_for, render_template
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

# URL/URIs for the API endpoints.
base_url = "http://127.0.0.1:5000"
low_sev_data = "/segments/low/"
mod_sev_data = "/segments/mod/"
high_sev_data = "/segments/mod"


@app.route("/")
def home():
    """Returns the HTML template for the homepage. Accepts GET requests only.
    :return: an HTML template.
    """
    return render_template("home.html")


@app.route("/customers/<severity>/<num_attributes>")
def customer_data(severity, num_attributes):
    """API endpoint that returns data depending on the exposure severity requested.
    :param severity: defines the severity of EDE, either none, low, mod or high.
    :param num_attributes: the number of attributes requested.
    :return: an HTML template, JSON response and HTTP status code.
    """
    if num_attributes in range(1, 7):
        if severity == "low":

            return status.HTTP_200_OK
        elif severity == "mod":
            return status.HTTP_200_OK
        elif severity == "high":
            return status.HTTP_200_OK
        elif severity == "none":
            return status.HTTP_200_OK
        else:
            return status.HTTP_400_BAD_REQUEST
    else:
        return status.HTTP_400_BAD_REQUEST



if __name__ == "__main__":
    app.run()
