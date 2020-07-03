import base64
import io
import json
import urllib

import matplotlib.pyplot as plt
import requests
from django.shortcuts import render

# TODO (D. Rodriguez 2020-06-30): Add error catching
# TODO (D. Rodriguez 2020-06-30): Improve looks
# TODO (D. Rodriguez 2020-06-30): Improve player list sorting

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


def get_player_list():
    """Gets full list of active and inactive players"""

    player_index_url = 'https://stats.nba.com/js/data/ptsd/stats_ptsd.js'
    response = requests.get(player_index_url, headers=HEADERS)

    player_data = json.loads(response.content.decode()[17:-1])

    # Return list of dictionaries with Player ID as key
    players = []
    all_players = player_data['data']['players']
    for player in all_players:
        players.append(
                {
                    'player_id': player[0],
                    'full_name': player[1],
                    'rookie_year': player[3],
                    'last_year': player[4],
                    'current_team_id': player[5],
                    }
                )

    return players


def get_player_common_info(player_id):
    """Get player details"""
    parameters = {
        'PlayerID': player_id
        }
    endpoint = 'commonplayerinfo'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = requests.get(request_url, headers=HEADERS, params=parameters)

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

    response = requests.get(request_url, headers=HEADERS, params=parameters)
    player_available_season_stats = json.loads(response.content.decode())['resultSets'][0]

    return player_available_season_stats


def get_player_game_log(player_id, season_year, season_type):
    parameters = {
        'DateFrom': '',
        'DateTo': '',
        'GameSegment': '',
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': '',
        'MeasureType': 'Base',
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'Totals',
        'Period': '0',
        'PlayerID': player_id,
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': season_year,
        'SeasonSegment': '',
        'SeasonType': season_type,
        'ShotClockRange': '',
        'VsConference': '',
        'VsDivision': ''
        }

    endpoint = 'playergamelogs'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = requests.get(request_url, headers=HEADERS, params=parameters)

    player_season_gamelog = json.loads(response.content.decode())['resultSets'][0]

    return player_season_gamelog


def get_player_shot_list(player_id, season_year, game_id):
    parameters = {
        'AheadBehind': '',
        'CFID': '',
        'CFPARAMS': '',
        'ClutchTime': '',
        'Conference': '',
        'ContextFilter': '',
        'ContextMeasure': 'FGA',
        'DateFrom': '',
        'DateTo': '',
        'Division': '',
        'EndPeriod': '1',
        'EndRange': '0',
        'GROUP_ID': '',
        'GameEventID': '',
        'GameID': game_id,
        'GameSegment': '',
        'GroupID': '',
        'GroupMode': '',
        'GroupQuantity': '0',
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': '',
        'Month': '0',
        'OnOff': '',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'Period': '0',
        'PlayerID': player_id,
        'PlayerID1': '',
        'PlayerID2': '',
        'PlayerID3': '',
        'PlayerID4': '',
        'PlayerID5': '',
        'PlayerPosition': '',
        'PointDiff': '',
        'Position': '',
        'RangeType': '0',
        'RookieYear': '',
        'Season': season_year,
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'ShotClockRange': '',
        'StartPeriod': '1',
        'StartRange': '0',
        'StarterBench': '',
        'TeamID': '0',
        'VsConference': '',
        'VsDivision': '',
        'VsPlayerID1': '',
        'VsPlayerID2': '',
        'VsPlayerID3': '',
        'VsPlayerID4': '',
        'VsPlayerID5': '',
        'VsTeamID': ''
        }

    endpoint = 'shotchartdetail'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = requests.get(request_url, headers=HEADERS, params=parameters)
    # clean_response = clean_data(response)
    # all_shot_data = clean_response['Shot_Chart_Detail']

    player_game_shot_list = json.loads(response.content.decode())['resultSets'][0]

    return player_game_shot_list


def get_game_box_score_summary(game_id):
    """Get game Box Score for specified game."""
    parameters = {
        'GameID': game_id,
        }

    endpoint = 'boxscoresummaryv2'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = requests.get(request_url, headers=HEADERS, params=parameters)
    # clean_response = clean_data(response)
    # all_shot_data = clean_response['Shot_Chart_Detail']

    game_box_score_summary = json.loads(
            response.content.decode()
            )['resultSets'][0]

    return game_box_score_summary


def plot_player_short_chart(player_game_shot_list, player_name, team_name,
                            matchup, game_date, scoring_headline):

    all_shot_data_list = []

    # name = player_game_shot_list['name']
    headers = player_game_shot_list['headers']
    row_set = player_game_shot_list['rowSet']

    for shot in row_set:
        all_shot_data_list.append(dict(zip(headers, shot)))

    x_all = []
    y_all = []

    x_made = []
    y_made = []

    x_miss = []
    y_miss = []

    for shot in all_shot_data_list:
        x_all.append(shot['LOC_X'])
        y_all.append(shot['LOC_Y'])

        if shot['SHOT_MADE_FLAG']:
            x_made.append(shot['LOC_X'])
            y_made.append(shot['LOC_Y'])
        else:
            x_miss.append(shot['LOC_X'])
            y_miss.append(shot['LOC_Y'])

    im = plt.imread('shotchart-blue.png')
    fig, ax = plt.subplots()
    ax.imshow(im, extent=[-260, 260, -65, 424])

    ax.scatter(x_miss, y_miss, marker='x', c='red')
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='green')

    plt.title(
            f'{player_name} ({team_name})\n'
            f'{scoring_headline}\n'
            f'{matchup} {game_date}'
            )

    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    # plt.show()
    return plt


# NOTE (D. Rodriguez 2020-06-28): context variable needs to be a list of
# dictionaries
def home(request):
    """Display player list."""
    player_list = get_player_list()

    context = {
        'player_list': player_list
        }

    return render(request, 'shotcharts/home.html', context)


def player_profile(request, player_id):
    """Display player season stats."""
    player_common_info, player_headline_stats = get_player_common_info(player_id)
    player_available_season_stats = get_player_seasons(player_id)

    context = {
        'player_common_info': player_common_info,
        'player_headline_stats': player_headline_stats,
        'player_available_season_stats': player_available_season_stats,
        }
    return render(request, 'shotcharts/player_profile.html', context)


def player_season_game_log(request, player_id, season_year):
    """Ger all games for a given season for a given player"""
    player_season_game_log = get_player_game_log(
            player_id,
            season_year,
            'Regular Season'
            )

    context = {
        'player_season_game_log': player_season_game_log,
        }
    return render(request, 'shotcharts/player_season_game_log.html', context)


def player_game_shot_list(request, player_id, season_year, game_id):
    """Get player specific game shot chart."""
    player_game_shot_list = get_player_shot_list(
            player_id,
            season_year,
            game_id)

    context = {
        'player_game_shot_list': player_game_shot_list,
        }
    return render(request, 'shotcharts/player_game_shot_list.html', context)


def player_game_shot_chart(request, player_id, season_year, game_id):
    """Plot game shot chart"""
    player_game_shot_list = get_player_shot_list(
            player_id,
            season_year,
            game_id)

    player_season_game_log = get_player_game_log(
            player_id,
            season_year,
            'Regular Season'
            )

    for game in player_season_game_log['rowSet']:
        if game_id in game:
            player_name = game[2]
            team_name = game[4]
            matchup = game[8]
            game_date = game[7][:10]
            scoring_headline = f'{game[30]} points on {game[11]}/{game[12]} shooting ' \
                               f'({game[14]}/{game[15]} from three)'

    plt = plot_player_short_chart(
            player_game_shot_list,
            player_name,
            team_name,
            matchup,
            game_date,
            scoring_headline,
            )

    # ======================================================================= #
    # NOTE (D. Rodriguez 2020-06-30): Tutorial for getting a matplotlib plot
    # to django template

    # plt.plot(range(10))

    fig = plt.gcf()

    # Convert graph into dtring buffer and then convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'shotcharts/player_game_shot_chart.html', {'data': uri})
    # ======================================================================= #


def about(request):
    return render(request, 'shotcharts/about.html')
