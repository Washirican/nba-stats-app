# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
# --------------------------------------------------------------------------- #
import requests
import json


def get_http_response(request_url, headers, parameters):
    errors = []

    try:
        response = requests.get(request_url, headers=headers, params=parameters)
        # response_data = response.json()
        return response
    except:
        errors.append('Unable to get URL.')
        return {'error': errors}
