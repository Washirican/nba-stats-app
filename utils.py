# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
# --------------------------------------------------------------------------- #
import requests
import json


def get_http_response(url):
    errors = []

    try:
        response = requests.get(url)
        response_data = response.json()
        return response_data
    except:
        errors.append('Unable to get URL.')
        return {'error': errors}
