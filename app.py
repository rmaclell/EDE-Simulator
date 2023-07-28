from flask import request, url_for, render_template
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)


@app.route("/")
def home():
    """Returns the HTML template for the homepage. Accepts GET requests only.
    :return: an HTML template.
    """
    return render_template("home.html")


@app.route("/collect/<severity>/<num_attributes>")
def collect_data(severity, num_attributes):
    """API endpoint that returns data depending on the exposure severity requested.
    :param severity: defines the severity of EDE, either none, low, mod or high.
    :param num_attributes: the number of attributes requested.
    :return: an HTML template, JSON response and HTTP status code.
    """
    if num_attributes in range(1, 5):
        if severity is "low":
            return status.HTTP_200_OK
        elif severity is "mod":
            return status.HTTP_200_OK
        elif severity is "high":
            return status.HTTP_200_OK
        elif severity is "none":
            return status.HTTP_200_OK
        else:
            return status.HTTP_400_BAD_REQUEST
    else:
        return status.HTTP_400_BAD_REQUEST
