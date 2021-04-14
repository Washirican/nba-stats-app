# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
from datetime import datetime, timedelta
from rq import Queue
from worker import conn
from flask import Flask
from utils import *

q = Queue(connection=conn)

player_id = 201939


def queue_tasks():
    result = q.enqueue(get_player_common_info, player_id)

    # Keep checking job status until it is finished
    while result.get_status() != 'finished':
        print('Waiting for results...')

    player_common_info = result.result[0]
    player_headline_stats = result.result[1]
    return player_common_info, player_headline_stats


if __name__ == "__main__":
    print('Starting everything...')
    player_common_info, player_headline_stats = queue_tasks()

    print(player_common_info)
    print(player_headline_stats)
