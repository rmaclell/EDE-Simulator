import json
import random
import sqlite3

import requests

# URL/URIs for the API endpoints.
base_url = "http://127.0.0.1:5000"
segments_uri = "/segments"


def get_attribute_list(severity_lvl):
    """Gets a list of attributes, formed from the columns defined in the relevant SQLite table.
    :param severity_lvl: a string value containing the severity level.
    :return:
    """
    attribute_list = []
    try:
        with sqlite3.connect('data/ede_eval_data') as connection:
            cur = connection.cursor()
            data = cur.execute("SELECT * FROM " + severity_lvl + "_severity")
            for attribute in data.description:
                attribute_list.append(attribute[0])
    except sqlite3.Error as err:
        raise SystemExit(err)
    return attribute_list


def generate_request_chain(severity_lvl, attribute_list, no_attributes):
    """Generates a pseudo-random request chain.
    :param severity_lvl: a string containing the severity of exposure selected. Verified before function call.
    :param attribute_list: a list containing the attributes requested.
    :param no_attributes: the number of attributes passed.
    :return: a string array containing the URIs for the request chain.
    """
    # Instantiate the maximum attributes, request chain list and base string for the URLs.
    max_attributes = no_attributes
    request_chain = []
    base_string = base_url + segments_uri + "/" + severity_lvl + "/?"

    # Create a copy of the attribute list to preserve the original.
    attributes_to_assign = attribute_list.copy()

    while max_attributes > 0:
        # Check the maximum attributes left is not one to prevent a value error in the random range function.
        if max_attributes != 1:
            no_req_attributes = random.randrange(1, max_attributes)
            req_attributes = random.sample(attributes_to_assign, no_req_attributes)
            new_request = base_string
            for attr_string in req_attributes:
                new_request = new_request + "attr=" + attr_string + "&"
                attributes_to_assign.remove(attr_string)
            new_request = new_request.rstrip(new_request[-1])
            max_attributes = max_attributes - no_req_attributes
            request_chain.append(new_request)
        else:
            new_request = base_string + "attr=" + attributes_to_assign[0]
            request_chain.append(new_request)
            break
    return request_chain


def handle_request_chain(request_chain):
    """Carries out GET requests for the given URIs in the request chain.
    :param request_chain: a string array containing the URIs to fetch.
    :return: a JSON response object.
    """
    response_data = {}
    for request_uri in request_chain:
        try:
            response = requests.get(request_uri)
            response_data.update(json.loads(response.json()))
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
    return response_data


def build_query_string(severity_lvl, attribute_list):
    """Builds an SQL query string depending on the attributes passed and the required severity level.
    :param severity_lvl: a string value containing the severity level.
    :param attribute_list: a list containing the attributes to be used in the column selection of the query
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


def fetch_data(severity_lvl, attribute_list):
    """Fetches data from SQLite database.
    :param severity_lvl: a string containing the severity level. Used to select the relevant table.
    :param attribute_list: a list containing the attributes. Used to build a query string containing the column names.
    :return: an SQLite cursor object.
    """
    try:
        with sqlite3.connect('data/ede_eval_data') as connection:
            cur = connection.cursor()
            cur.execute(build_query_string(severity_lvl, attribute_list))
    except sqlite3.Error as err:
        raise SystemExit(err)
    return cur


def construct_json_response(cursor):
    """Constructs a JSON response with key:value pairs from the SQLite cursor given.
    :param cursor: a SQLite cursor object
    :return: a JSON object containing the fetched data.
    """
    # Extracts the column name and row values to insert into key:value pairs.
    response = [dict((cursor.description[i][0], value)
                     for i, value in enumerate(row)) for row in cursor.fetchall()]
    return json.dumps(response[0])


