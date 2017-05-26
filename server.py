import logging
from threading import Lock

import cli_args  as cli
import unicornhat as unicorn
from cli_args import LOG_LEVEL
from cli_args import setup_cli_args
from flask import Flask
from flask import make_response
from flask import request
from utils import setup_logging

logger = logging.getLogger(__name__)

page_cache = {}
cache_lock = Lock()
file_lock = Lock()

flask = Flask(__name__)


@flask.route("/clear")
def clear():
    unicorn.clear()
    return response()


@flask.route("/show")
def show():
    unicorn.show()
    return response()


@flask.route("/x")
def x():
    return response(unicorn.get_shape()[0])


@flask.route("/y")
def y():
    return response(unicorn.get_shape()[1])


@flask.route("/set_all")
def set_all():
    r = request.args.get("r")
    g = request.args.get("g")
    b = request.args.get("b")
    unicorn.set_all(r=int(r), g=int(g), b=int(b))
    return response()


@flask.route("/set_pixel")
def set_pixel():
    x = request.args.get("x")
    y = request.args.get("y")
    r = request.args.get("r")
    g = request.args.get("g")
    b = request.args.get("b")
    unicorn.set_pixel(x=int(x), y=int(y), r=int(r), g=int(g), b=int(b))
    return response()


@flask.route("/get_pixel")
def get_pixel():
    x = request.args.get("x")
    y = request.args.get("y")
    val = str(unicorn.get_pixel(x=int(x), y=int(y)))[1:-1]
    return response(val)


@flask.route("/rotation/<int:rotation>")
def brigtness(rotation):
    unicorn.rotation(rotation)
    return response()


@flask.route("/brightness/<float:brightness>")
def brigtness(brightness):
    unicorn.brightness(brightness)
    return response("")


@flask.route("/get_brightness")
def get_brightness():
    return response(unicorn.get_brightness())


def response(val=""):
    resp = make_response(str(val), 200)
    resp.headers["Content-Type"] = "text/plain"
    resp.headers["Access-Control-Allow-Origin"] = "http://snap.berkeley.edu"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return resp


if __name__ == "__main__":
    args = setup_cli_args(cli.verbose)

    setup_logging(level=args[LOG_LEVEL])

    flask.run(host="0.0.0.0", port=9000)
