import gevent
from gevent import monkey
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import redis


app = Flask(__name__)
app.debug = True
monkey.patch_all()
red = lambda: redis.Redis()


@app.route('/')
def index():
    return render_template('index.html')


def listener(websocket):
    sub = red().pubsub()
    sub.subscribe('ecg')

    for message in sub.listen():
        websocket.send(message['data'])


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


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
