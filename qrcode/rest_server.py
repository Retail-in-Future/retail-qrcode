import os
import string
import random
from json import JSONEncoder, JSONDecoder

import boto3
from eve import Eve
from flask import request
from qrcode.utils import read_yaml_config
import redis


_CONFIG = read_yaml_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'))
_APP = Eve(settings="qrcode/settings.py")
_REDIS = redis.Redis(host='redis', port=6379, db=0)


def generate_toke(len_):
    return ''.join(random.sample(string.digits + string.ascii_letters, len_))


@_APP.route("/token", methods=["POST"])
def token_request_hdl():
    if request.method == "POST":
        uid_json = request.get_json(force=True, silent=True)
        if uid_json is None:
            return "Illegal json format", 400

        uid = uid_json.get("uid", None)
        if uid is not None:
            token = generate_toke(_CONFIG["token_length"])
            _REDIS.set(uid, token, ex=_CONFIG["token_expired"])
            return JSONEncoder().encode({"token": token}), 200
        else:
            return "lost uid", 400

    else:
        return "invalid http method, must be post", 400


# qrcode format: uid$token
@_APP.route("/gates_status", methods=["POST"])
def gates_status_request_hdl():
    if request.method == "POST":
        body = request.get_json(force=True, silent=True)
        if body is None:
            return "lost body", 400

        payload = JSONDecoder().decode(body)

        dev_attri = payload.get("dev", None)
        qrcode_attri = payload.get("qrcode", None)
        if dev_attri is None or qrcode_attri is None:
            return "lost dev or qrcode", 400

        qrcode_l = qrcode_attri.split("$", 1)
        if len(qrcode_l) != 2:
            return "Illegal qrcode format ", 400



        return "", 200

    else:
        return "invalid http method, must be post", 400


def start_server():
    _APP.run(host="0.0.0.0")


if __name__ == "__main__":
    start_server()
