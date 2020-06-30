# --------------------------------------------------------------------------- #
# D. Rodriguez, 2020-06-28, File created.
# --------------------------------------------------------------------------- #
"""Get player data by player full name (last, first)"""

import requests
import json

from teams import Teams


class Player:
    """Simple player class."""

    __HEADERS = {
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

    def __init__(self, player_name):
        """Constructor for Player"""

        # TODO (D. Rodriguez 2020-05-14): Move code to
        #  get_player_basic_info() method. Leave only parameter
        #  initialization here.
        #  Is this necessary?

        # Initialize variables to be set by code
        self.full_name = player_name

        self.seasons_played = []
        self.season_totals = {}

        player_index_url = 'https://stats.nba.com/js/data/ptsd/stats_ptsd.js'
        player_list = requests.get(player_index_url)

        # Cleanup string
        player_data = json.loads(player_list.content.decode()[17:-1])

        # Turns string into dictionary
        # player_data = json.loads(player_data_str)

        # Extracts data from dictionary
        players = player_data['data']['players']
        teams = player_data['data']['teams']
        self.data_date = player_data['generated']

        # TODO (D. Rodriguez 2020-05-14): Implement error handling if
        #  Player Name is not found.

        # TODO (D. Rodriguez 2020-05-14): Improve search performance.
        #  Implement binary search?
        for player in players:
            if self.full_name == player[1]:
                self.id = player[0]
                self.rookie_season = player[3]
                self.last_season = player[4]
                self.current_team_id = player[5]

                break

        if self.current_team_id != 0:
            team = Teams(self.current_team_id)
            self.current_team_abbreviation = team.abbreviation
            self.current_team_city = team.city
            self.current_team_nickname = team.nickname
        else:
            self.current_team_abbreviation = ''
            self.current_team_city = ''
            self.current_team_nickname = ''

    def get_player_basic_info(self):
        """Gets basic player data (Rookie season, team)"""
        pass

    def get_player_seasons_played(self):
        """Get player season years played."""
        self.seasons_played = list(self.season_totals.keys())

    def get_player_per_season_totals(self):
        """Get player season totals per player ID"""
        parameters = {
            'LeagueID': '00',
            'PerMode': 'PerGame',
            'PlayerID': self.id,
            }

        endpoint = 'playerprofilev2'
        request_url = f'https://stats.nba.com/stats/{endpoint}?'

        response = requests.get(request_url, headers=Players.__HEADERS,
                                params=parameters)

        season_totals_headers = json.loads(
                response.content.decode())['resultSets'][0]['headers']

        season_totals_values = json.loads(
                response.content.decode())['resultSets'][0][
            'rowSet']

        # self.season_totals = {}

        for season in season_totals_values:
            self.season_totals[season[1]] = dict(
                    zip(season_totals_headers, season))

        # return self.season_totals
