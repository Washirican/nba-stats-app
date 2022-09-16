# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
from datetime import datetime, timedelta
from rq import Queue
from worker import conn
from flask import Flask, render_template, request, Response
from utils import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """"""
    # player_id = 201939

    # player_common_info, player_headline_stats = get_player_common_info(player_id)

    player_index_url = "https://stats.wnba.com/js/data/ptsd/stats_ptsd.js"
    player_list = requests.get(player_index_url)
    player_data = json.loads(player_list.content.decode()[17:-1])

    # Extracts data from dictionary
    players = player_data['data']['players']
    teams = player_data['data']['teams']
    data_date = player_data['generated']

    return render_template('index.html',
                           content=players)

    # return render_template('player_profile.html',
    #                        player_common_info=player_common_info,
    #                        player_headline_stats=player_headline_stats)


if __name__ == "__main__":
    # print('Starting everything...')
    # player_common_info, player_headline_stats = queue_tasks()
    #
    # print(player_common_info)
    # print(player_headline_stats)

    app.run(debug=True)
