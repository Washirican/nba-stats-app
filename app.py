# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
from rq import Queue
from worker import conn
from utils import *

q = Queue(connection=conn)

player_id = 201939

result = q.enqueue(get_player_common_info, player_id)

# print(result)
player_common_info, player_headline_stats = result.result
print(player_headline_stats)
