# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
# --------------------------------------------------------------------------- #
import json
from flask import Flask, render_template, request, Response
from utils import get_http_response

app = Flask(__name__)

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


# TODO (D. Rodriguez 2021-04-09): Implement background task (Redis?)
#  queue to avoid timeout error.
def get_player_common_info(player_id):
    """Get player details"""
    parameters = {
        'PlayerID': player_id
        }
    endpoint = 'commonplayerinfo'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    # response = requests.get(request_url, headers=HEADERS, params=parameters)
    response = get_http_response(request_url, HEADERS, parameters)

    player_common_info = json.loads(response.content.decode())['resultSets'][0]
    player_headline_stats = json.loads(response.content.decode())['resultSets'][1]

    return player_common_info, player_headline_stats


def get_player_seasons(player_id):
    """Get player season's played per player ID"""
    parameters = {
        'LeagueID': '00',
        'PerMode': 'PerGame',
        'PlayerID': player_id
        }

    endpoint = 'playerprofilev2'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = get_http_response(request_url, HEADERS, parameters)
    player_available_season_stats = json.loads(response.content.decode())['resultSets'][0]

    return player_available_season_stats


@app.route('/', methods=['GET'])
def index():
    parameters = {}
    player_index_url = 'https://stats.nba.com/js/data/ptsd/stats_ptsd.js'
    player_list = get_http_response(player_index_url, HEADERS, parameters)

    dict_str = player_list.content.decode()[17:-1]

    # Turns string into dictionary
    data = json.loads(dict_str)
    all_players = data['data']['players']
    player_list = []

    for player in all_players:
        player_list.append(
                {
                    'player_id': player[0],
                    'full_name': player[1],
                    'rookie_year': player[3],
                    'last_year': player[4],
                    'current_team_id': player[5],
                    }
                )

    # teams = data['data']['teams']
    # data_date = data['generated']
    # content = player_list

    return render_template('index.html', content=player_list)


@app.route('/player_profile/<player_id>', methods=['GET'])
def player_profile(player_id):
    """Display player season stats."""
    # player_id = 201939
    player_id = player_id

    player_common_info, player_headline_stats = get_player_common_info(player_id)
    player_available_season_stats = get_player_seasons(player_id)

    return render_template('player_profile.html',
                           player_common_info=player_common_info,
                           player_headline_stats=player_headline_stats,
                           player_available_season_stats=player_available_season_stats
                           )


if __name__ == '__main__':
    app.run(debug=True)
