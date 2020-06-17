import os

from flask import Flask, request, jsonify, abort, redirect, url_for, render_template
from flask_redis import FlaskRedis
import redis


app = Flask(__name__)
redis_client = FlaskRedis(app)

APP_HEALTH_OK = True
APP_VERSION = 1.0
FEATURES = [ (feat, os.environ.get(feat)) for feat in os.environ if feat.startswith("FEAT_")]

@app.route("/")
def index():
    try:
        redis_client.incr("counter")
        current_hits = redis_client.get("counter").decode()
    except redis.ConnectionError:
        current_hits = "not available"

    if request.is_json:
        return redirect(url_for("version"))
    else:
        return render_template('index.html',
                            version=APP_VERSION,
                            name=os.environ.get("HOSTNAME", "localhost"),
                            features=dict(FEATURES),
                            current_hits=current_hits)

@app.route("/version")
def version():
    try:
        current_hits = redis_client.get("counter").decode() or 0
    except redis.ConnectionError:
        current_hits=None
    return jsonify(version=APP_VERSION, features=FEATURES,
        hostname=os.environ.get("HOSTNAME", "localhost"),
        hits=current_hits)

@app.route("/healthz")
def healthz():
    if APP_HEALTH_OK:
        return jsonify(healthy=APP_HEALTH_OK)
    else:
        abort(500)

@app.route("/reset")
def reset():
    try:
        redis_client.set("counter", 0)
    except redis.ConnectionError:
        abort(500)
    else:
        return("OK")

@app.route("/invalidate")
def invalidate():
    global APP_HEALTH_OK
    APP_HEALTH_OK = False

    abort(500)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)