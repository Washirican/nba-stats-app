# --------------------------------------------------------------------------- #
# D. Rodriguez, 2020-06-28, File created.
# --------------------------------------------------------------------------- #

"""Get team data by team ID"""
import requests
import json


class Team:
    """Get team data from team ID"""

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

    def __init__(self, team_id):
        """Constructor for Teams"""
        self.id = team_id

        parameters = {'teamID': self.id}

        endpoint = 'teamdetails'
        request_url = f'https://stats.nba.com/stats/{endpoint}?'

        # TODO (D. Rodriguez 2020-05-14): Implement error handling if
        #  Team ID is not found

        # TODO (D. Rodriguez 2020-05-14): Move code to method?


        response = requests.get(request_url, headers=Teams.__HEADERS,
                                params=parameters)

        team_data_headers = \
        json.loads(response.content.decode())['resultSets'][0]['headers']
        team_data_values = json.loads(response.content.decode())['resultSets'][0][
            'rowSet'][0]

        team_data_dict = dict(zip(team_data_headers, team_data_values))

        self.abbreviation = team_data_dict['ABBREVIATION']
        self.nickname = team_data_dict['NICKNAME']
        self.year_founded = team_data_dict['YEARFOUNDED']
        self.city = team_data_dict['CITY']
        self.arena = team_data_dict['ARENA']
        self.arena_capacity = team_data_dict['ARENACAPACITY']
        self.owner = team_data_dict['OWNER']
        self.general_manager = team_data_dict['GENERALMANAGER']
        self.head_coach = team_data_dict['HEADCOACH']
        self.d_league_affiliation = team_data_dict['DLEAGUEAFFILIATION']

    def get_team_basic_data(self):
        """"""
        pass
