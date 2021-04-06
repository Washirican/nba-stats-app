# --------------------------------------------------------------------------- #
# D. Rodriguez, 2021-04-06, File created.
# --------------------------------------------------------------------------- #
from flask import Flask, render_template, request, Response
from utils import get_http_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
