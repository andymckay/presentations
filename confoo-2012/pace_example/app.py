from flask import Flask, render_template

import gevent
from gevent import monkey

import redis

app = Flask(__name__)


def listener():
    sub = redis.Redis().pubsub()
    sub.subscribe('testing')

    for message in sub.listen():
        print message


@app.route('/')
def index():
    gevent.spawn(listener)
    return render_template('index.html')


if __name__ == "__main__":
    monkey.patch_all()
    app.debug = True
    app.run()
