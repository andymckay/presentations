from flask import Flask, request, render_template

import gevent
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from gevent import monkey

import redis

app = Flask(__name__)

conn = redis.Redis()


def listener(websocket, key):
    sub = redis.Redis().pubsub()
    sub.subscribe(key)

    for message in sub.listen():
        websocket.send('ecg-data-%s' % message['data'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/')
def api():
    websocket = request.environ.get('wsgi.websocket', None)
    if websocket:
        greenlet = None
        while True:
            message = websocket.receive()
            # On connected send they keys.
            if message == 'connected':
                websocket.send('ecgs-keys-%s' %
                               '|'.join(conn.smembers('ecgs-keys')))

            # Kill the greenlet or start a new one
            elif message in conn.smembers('ecgs-keys'):
                if greenlet:
                    greenlet.kill(gevent.Greenlet.GreenletExit)
                greenlet = gevent.spawn(listener, websocket,
                                        'ecg-%s' % message)

            elif message is None and greenlet:
                greenlet.throw(gevent.Greenlet.GreenletExit)
                break

    return ''

if __name__ == "__main__":
    monkey.patch_all()
    app.debug = True
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
