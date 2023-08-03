import json
import random
import sqlite3

import requests

# URL/URIs for the API endpoints.
base_url = "http://127.0.0.1:5000"
segments_uri = "/segments"


def get_attribute_list(severity):
    attribute_list = []
    with sqlite3.connect('data/ede_eval_data') as connection:
        cur = connection.cursor()
        data = cur.execute("SELECT * FROM " + severity + "_severity")
        for attribute in data.description:
            attribute_list.append(attribute[0])
    return attribute_list


def fetch_data(severity, attribute_list):
    with sqlite3.connect('data/ede_eval_data') as connection:
        cur = connection.cursor()
        cur.execute(build_query_string(attribute_list, severity))
    return cur


def generate_request_chain(severity, attributes, no_attributes):
    """Creates a pseudo-random request chain for internal services.
    :param no_attributes:
    :param attributes:
    :param severity: the severity of exposure selected.
    :return: a string array containing the URIs for the request chain.
    """
    # Instantiate the maximum attributes and the request chain array.
    max_attributes = no_attributes
    request_chain = []
    base_string = base_url + segments_uri + "/" + severity + "/?"

    while max_attributes > 0:
        # Check the maximum attributes left is not one to prevent a value error in the random range function.
        if max_attributes != 1:
            no_req_attributes = random.randrange(1, max_attributes)
            req_attributes = random.sample(attributes, no_req_attributes)
            new_request = base_string
            for attr_string in req_attributes:
                new_request = new_request + "attr=" + attr_string + "&"
                attributes.remove(attr_string)
            new_request = new_request.rstrip(new_request[-1])
            max_attributes = max_attributes - no_req_attributes
            request_chain.append(new_request)
        else:
            new_request = base_string + "attr=" + attributes[0]
            request_chain.append(new_request)
            break
    return request_chain


def handle_request_chain(request_chain):
    response_data = {}
    for request_uri in request_chain:
        response = requests.get(request_uri)
        response_data.update(json.loads(response.json()))
    return response_data


def construct_json_response(cursor):
    response = [dict((cursor.description[i][0], value)
                     for i, value in enumerate(row)) for row in cursor.fetchall()]
    return json.dumps(response[0])


def build_query_string(attribute_list, severity_lvl):
    """Builds an SQL query string depending on the attributes passed and the requried severity level.
    :param attribute_list: a list containing the attributes to be used in the column selection of the query
    :param severity_lvl: a string value containing the severity level.
    :return: a string containing the SQL query.
    """
    table_string = severity_lvl + "_severity"
    column_string = attribute_list[0]
    if len(attribute_list) > 1:
        for attr_string in attribute_list:
            column_string = column_string + "," + attr_string
    return ("SELECT " + column_string + " FROM " + table_string +
            " WHERE ROWID IN (SELECT ROWID from " + table_string +
            " ORDER BY random() LIMIT 1)")
