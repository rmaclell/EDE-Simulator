import json
import sqlite3
import requests
from flask import Flask, request, url_for, render_template
from flask_api import FlaskAPI, status, exceptions
from internal_services import generate_request_chain, construct_json_response, build_query_string

app = Flask(__name__)

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


@app.route("/customers/<severity>/<int:num_attributes>")
def customer_data(severity, num_attributes):
    """API endpoint that returns data depending on the exposure severity requested.
    :param severity: defines the severity of EDE, either none, low, mod or high.
    :param num_attributes: the number of attributes requested.
    :return: an HTML template, JSON response and HTTP status code.
    """
    if num_attributes in range(1, 7):
        with sqlite3.connect('data/ede_eval_data') as connection:
            cur = connection.cursor()
            if severity == "low":
                low_sev_attributes = []
                data = cur.execute("SELECT * FROM low_severity")
                for attribute in data.description:
                    low_sev_attributes.append(attribute[0])
                request_chain = generate_request_chain(severity, low_sev_attributes)
                response_data = {}
                for request_uri in request_chain:
                    response = requests.get(request_uri)
                print(response_data)
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


customer_data("low", 5)


@app.route("/segments/low/")
def customer_segments_low():
    attribute_list = request.args.getlist("attr")
    with sqlite3.connect('data/ede_eval_data') as connection:
        cur = connection.cursor()
        cur.execute(build_query_string(attribute_list, "low"))
        connection.commit()
        response = construct_json_response(cur)
        return response[0]


@app.route("/segments/mod/<num_attributes>")
def customer_segments_mod(num_attributes):
    if num_attributes in range(1, 7):
        cur.execute("SELECT * FROM mod_severity")
        return status.HTTP_200_OK
    else:
        return status.HTTP_400_BAD_REQUEST


@app.route("/segments/high/<num_attributes>")
def customer_segments_high(num_attributes):
    if num_attributes in range(1, 7):
        cur.execute("SELECT * FROM high_severity")
        return status.HTTP_200_OK
    else:
        return status.HTTP_400_BAD_REQUEST


if __name__ == "__main__":
    app.run()
