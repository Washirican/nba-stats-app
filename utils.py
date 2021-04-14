# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
# --------------------------------------------------------------------------- #
import requests
import json

HEADERS = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) '
                      'Gecko/20100101 Firefox/72.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://stats.nba.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        }


# def get_http_response(request_url, headers, parameters):
#     errors = []
#
#     try:
#         response = requests.get(request_url, headers=headers, params=parameters)
#         response_data = response.json()
        # return response
    # except:
    #     errors.append('Unable to get URL.')
    #     return {'error': errors}


# TODO (D. Rodriguez 2021-04-09): Implement background task (Redis?)
#  queue to avoid timeout error.
def get_player_common_info(player_id):
    """Get player details"""

    # print("\nStarting get_player_common_info() task...")

    parameters = {
        'PlayerID': player_id
        }
    endpoint = 'commonplayerinfo'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = requests.get(request_url, headers=HEADERS, params=parameters)
    # response = get_http_response(request_url, HEADERS, parameters)

    player_common_info = json.loads(response.content.decode())['resultSets'][0]
    player_headline_stats = json.loads(response.content.decode())['resultSets'][1]

    # print('\n')
    # print(player_common_info)
    # print('\n')
    # print(player_headline_stats)
    # print('\n')

    return player_common_info, player_headline_stats


def get_player_seasons(player_id):
    """Get player season's played per player ID"""

    # print("\nStarting get_player_seasons() task...")

    parameters = {
        'LeagueID': '00',
        'PerMode': 'PerGame',
        'PlayerID': player_id
        }

    endpoint = 'playerprofilev2'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = requests.get(request_url, headers=HEADERS, params=parameters)
    # response = get_http_response(request_url, HEADERS, parameters)

    player_available_season_stats = json.loads(response.content.decode())['resultSets'][0]

    # print('\n')
    # print(player_available_season_stats)
    # print('\n')

    return player_available_season_stats
