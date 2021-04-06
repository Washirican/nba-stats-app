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


@app.route('/', methods=['GET', 'POST'])
def index():
    player_index_url = 'https://stats.nba.com/js/data/ptsd/stats_ptsd.js'
    player_list = get_http_response(player_index_url)

    dict_str = player_list.content.decode()[17:-1]

    # Turns string into dictionary
    data = json.loads(dict_str)

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
