import http
import random
from flask import Flask, request, url_for, render_template, jsonify
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


@app.route("/customers/<severity_lvl>/<int:num_attributes>")
def customer_data(severity_lvl, num_attributes):
    """API endpoint for the customer data resource. Accepts GET requests only.
    :param severity_lvl: defines the severity of EDE, either none, low, mod or high.
    :param num_attributes: the number of attributes requested.
    :return: an HTML template, JSON response and HTTP status code.
    """
    if num_attributes in range(_MIN_ATTRIBUTES, _MAX_ATTRIBUTES + 1):
        if severity_lvl in _SEVERITY_LVLS:
            attribute_list = get_attribute_list(severity_lvl)
            request_chain = generate_request_chain(severity_lvl, attribute_list, len(attribute_list))
            response_data = handle_request_chain(request_chain)
            return jsonify(http.HTTPStatus.OK.value, response_data)
        elif severity_lvl == "none":
            selected_entity = random.choice(_SEVERITY_LVLS)
            attribute_list = get_attribute_list(selected_entity)
            selected_attributes = random.sample(attribute_list, num_attributes)
            request_chain = generate_request_chain(selected_entity, selected_attributes, len(selected_attributes))
            response_data = handle_request_chain(request_chain)
            return jsonify(http.HTTPStatus.OK.value, response_data)
        else:
            return jsonify(http.HTTPStatus.BAD_REQUEST.value, "The security level requested is not recognised.")
    else:
        return jsonify(http.HTTPStatus.BAD_REQUEST.value, "The requested URL is malformed.")


@app.route("/segments/<severity_lvl>/")
def customer_segments(severity_lvl):
    """API endpoint for the customer segments resource.
    :param severity_lvl: a string defining the
    :return: a JSON response object.
    """
    if severity_lvl in _SEVERITY_LVLS:
        attribute_list = request.args.getlist("attr")
        data = fetch_data(severity_lvl, attribute_list)
        response = construct_json_response(data)
        return jsonify(response)
    else:
        return jsonify(http.HTTPStatus.BAD_REQUEST.value, "The security level requested is not recognised.")


if __name__ == "__main__":
    app.run()
