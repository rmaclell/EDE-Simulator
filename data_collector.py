import random
import sqlite3
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from app import app

# Establish a connection to the local SQLite database.
connection = sqlite3.connect('data/ede_eval_data')
cur = connection.cursor()

# Variables containing literals for conditional statements.
req_attr_one = 1
req_attr_two = 2
req_attr_three = 3
req_attr_four = 4
req_attr_five = 5
req_attr_six = 6
req_attr_seven = 7
_MAX_ATTRIBUTES = 7

# URL/URIs for the API endpoints.
base_url = "http://127.0.0.1:5000"
segments_uri = "/segments"


def generate_request_chain(severity):
    # Instantiate the number of requests to be generated and the request chain array.
    gt_one_req = bool(random.getrandbits(1))
    max_attributes = 7
    req_attributes = max_attributes
    request_chain = []

    while max_attributes > 0:
        if max_attributes != 1:
            req_attributes = random.randrange(1, max_attributes)
            new_request = base_url + segments_uri + "/" + severity + "/" + str(req_attributes)
            max_attributes = max_attributes - req_attributes
            request_chain.append(new_request)
        else:
            new_request = base_url + segments_uri + "/" + severity + "/" + str(req_attributes)
            request_chain.append(new_request)
    return request_chain


print(generate_request_chain("low"))


@app.route("/segments/low/<num_attributes>")
def customer_segments_low(num_attributes):
    if num_attributes in range(1, 7):
        cur.execute("SELECT * FROM low_severity")
        return status.HTTP_200_OK
    else:
        return status.HTTP_400_BAD_REQUEST


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
