import http
import os
import random
from flask import Flask, request, render_template, jsonify, session
from internal_services import generate_request_chain, construct_json_response, handle_request_chain, get_attribute_list, \
    fetch_data, filter_attributes

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12).hex()

_MIN_ATTRIBUTES = 1
_MAX_ATTRIBUTES = 5
_SEVERITY_LVLS = ["low", "mod", "high"]
_HIDE_ELEMENTS = ["Request", "Response", "Filter", "Attributes"]


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
            consumed_attributes, unconsumed_attributes = filter_attributes(num_attributes, attribute_list)
            request_chain = generate_request_chain(severity_lvl, attribute_list, len(attribute_list))
            response_data = handle_request_chain(request_chain)
            return render_template("home.html", request_url=request.url, request_method=request.method,
                                   response_data=response_data, num_attributes=num_attributes,
                                   attribute_list=attribute_list, consumed_attributes=consumed_attributes,
                                   unconsumed_attributes=unconsumed_attributes, status=http.HTTPStatus.OK.value)
        elif severity_lvl == "none":
            selected_entity = random.choice(_SEVERITY_LVLS)
            attribute_list = get_attribute_list(selected_entity)
            selected_attributes = random.sample(attribute_list, num_attributes)
            request_chain = generate_request_chain(selected_entity, selected_attributes, len(selected_attributes))
            response_data = handle_request_chain(request_chain)
            return render_template("home.html", request_url=request.url, request_method=request.method,
                                   response_data=response_data, num_attributes=num_attributes,
                                   attribute_list=selected_attributes, status=http.HTTPStatus.OK.value)
        else:
            return render_template('home.html', status_value=http.HTTPStatus.BAD_REQUEST.value,
                                   status_desc=http.HTTPStatus.BAD_REQUEST.description, request_url=request.url,
                                   error="The severity level requested is not recognised.")
    else:
        if severity_lvl in _SEVERITY_LVLS:
            return render_template('home.html', status_value=http.HTTPStatus.BAD_REQUEST.value,
                                   status_desc=http.HTTPStatus.BAD_REQUEST.description, request_url=request.url,
                                   error="The number of attributes requested is invalid.")
        else:
            return render_template('home.html', status_value=http.HTTPStatus.BAD_REQUEST.value,
                                   status_desc=http.HTTPStatus.BAD_REQUEST.description, request_url=request.url,
                                   error="The severity level is not recognised and the number of attributes requested "
                                         "is invalid.")


@app.route("/segments/<severity_lvl>/")
def customer_segments(severity_lvl):
    """API endpoint for the customer segments resource.
    :param severity_lvl: a string defining the severity level.
    :return: a JSON response object.
    """
    if severity_lvl in _SEVERITY_LVLS:
        attribute_list = request.args.getlist("attr")
        data = fetch_data(severity_lvl, attribute_list)
        response = construct_json_response(data)
        return jsonify(response)
    else:
        return jsonify(http.HTTPStatus.BAD_REQUEST.value, "The security level requested is not recognised.")


@app.route("/session/")
def manage_session():
    if request.args.get("hide_button"):
        if request.args.get("hide_button") == "True" or "False":
            session['HIDE_BUTTON'] = request.args.get("hide_button")
            print(session)
            return render_template("home.html")
        else:
            return render_template("home.html")
    elif request.args.get("hide_element"):
        if request.args.get("hide_element") in _HIDE_ELEMENTS:
            hidden_elements = session.get("HIDDEN_ELEMENTS")
            hidden_elements.append(request.args.get("hide_element"))
            session["HIDDEN_ELEMENTS"] = hidden_elements
            print(session)
    elif request.args.get("unhide_element"):
        if request.args.get("unhide_element") in _HIDE_ELEMENTS:
            hidden_elements = session.get("HIDDEN_ELEMENTS")
            hidden_elements.remove(request.args.get("unhide_element"))
            session["HIDDEN_ELEMENTS"] = hidden_elements
            print(session)
    elif request.args.get("clear"):
        if request.args.get("clear") == "True":
            session.clear()
            return render_template("home.html")
        else:
            return render_template("home.html")
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run()
