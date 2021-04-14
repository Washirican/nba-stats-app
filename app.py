# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
from datetime import datetime, timedelta
from rq import Queue
from worker import conn
from flask import Flask, render_template, request, Response
from utils import *

app = Flask(__name__)

q = Queue(connection=conn)


def queue_tasks(player_id):
    result = q.enqueue(get_player_common_info, player_id)

    # Keep checking job status until it is finished
    while result.get_status() != 'finished':
        # TODO (D. Rodriguez 2021-04-14): Revise this
        print('Waiting for results...')

    player_common_info = result.result[0]
    player_headline_stats = result.result[1]
    return player_common_info, player_headline_stats


@app.route('/', methods=['GET', 'POST'])
def index():
    """"""
    player_id = 201939

    player_common_info, player_headline_stats = queue_tasks(player_id)

    return render_template('player_profile.html',
                           player_common_info=player_common_info,
                           player_headline_stats=player_headline_stats)


if __name__ == "__main__":
    # print('Starting everything...')
    # player_common_info, player_headline_stats = queue_tasks()
    #
    # print(player_common_info)
    # print(player_headline_stats)

    app.run(debug=True)

