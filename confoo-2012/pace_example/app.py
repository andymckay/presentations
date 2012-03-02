from flask import Flask, render_template

import redis

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', test=redis.Redis().get('test'))


if __name__ == "__main__":
    app.debug = True
    app.run()
