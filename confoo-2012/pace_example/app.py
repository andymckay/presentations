from flask import Flask, request, render_template

import gevent
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from gevent import monkey

import redis

app = Flask(__name__)


def listener(websocket):
    sub = redis.Redis().pubsub()
    sub.subscribe('testing')

    for message in sub.listen():
        websocket.send(message['data'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/')
def api():
    websocket = request.environ.get('wsgi.websocket', None)
    if websocket:
        greenlet = gevent.spawn(listener, websocket)
        while True:
            message = websocket.receive()
            if message is None:
                greenlet.throw(gevent.Greenlet.GreenletExit)
                break

    return ''

if __name__ == "__main__":
    monkey.patch_all()
    app.debug = True
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
