import random
import sqlite3
from flask import Flask, request, url_for, render_template, jsonify
from flask_api import FlaskAPI, status, exceptions
from internal_services import generate_request_chain, construct_json_response, handle_request_chain, get_attribute_list, \
    fetch_data

app = Flask(__name__)

_MIN_ATTRIBUTES = 1
_MAX_ATTRIBUTES = 7
_SEVERITY_LVLS = ["low", "mod", "high"]


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
    if num_attributes in range(_MIN_ATTRIBUTES, _MAX_ATTRIBUTES + 1):
        if severity in _SEVERITY_LVLS:
            attribute_list = get_attribute_list(severity)
            request_chain = generate_request_chain(severity, attribute_list, len(attribute_list))
            response_data = handle_request_chain(request_chain)
            return jsonify(status.HTTP_200_OK, response_data)
        elif severity == "none":
            selected_entity = random.choice(_SEVERITY_LVLS)
            attribute_list = get_attribute_list(selected_entity)
            selected_attributes = random.sample(attribute_list, num_attributes)
            request_chain = generate_request_chain(selected_entity, selected_attributes, len(selected_attributes))
            response_data = handle_request_chain(request_chain)
            return jsonify(status.HTTP_200_OK, response_data)
        else:
            return jsonify(status.HTTP_400_BAD_REQUEST, "The security level requested is not recognised."),
    else:
        return jsonify(status.HTTP_400_BAD_REQUEST, "The requested URL is malformed.")


@app.route("/segments/<severity>/")
def customer_segments(severity):
    attribute_list = request.args.getlist("attr")
    data = fetch_data(severity, attribute_list)
    response = construct_json_response(data)
    return jsonify(response)


if __name__ == "__main__":
    app.run()
