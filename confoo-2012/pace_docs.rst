Pace Example from Confoo 2012
-----------------------------

Before the presentation the following is assumed:

- On OS X (this only affects the redis install, which should be pretty easy in
  the packaging system for your os of choice).

- Have Python 2.6+ installed.

- Have PIP installed::

        easy_install pip

- Before I started I set::

        export PIP_DOWNLOAD_CACHE=~/.pip/download_cache

So that in theory everything would still work if the intertubes went down.

Step 1: Stand up Flask
-----------------------------
Run::

        git checkout 2281c8157112b79be7aa499c51d30e0db3adc006

Setup a virtualenv [1]_ [2]_::

        pip install virtualenv
        pip install virtualenvwrapper

Create a new virtualenv::

        mkvirtualenv pace

Activate the new virtualenv[3]_::

        workon pace

We'll be using Flask [4]_::

        pip install Flask

Add in "Hello World". Run::

        python app.py

Open a browser::

        http://localhost:5000/

Optionally, run using gunicorn::

        pip install gunicorn

Run using gunicorn::

        gunicorn app:app

Step 2: Hooking up redis to python
----------------------------------

Run::

        git checkout c1a02dff4755bb60e2a3cb0078fc4afea7e4f089

Hooking up to Redis [5]_. Install redis (OS X specific) using homebrew [6]_::

        brew install redis

Once its done [7]_::

        brew info redis

Let's start Redis manually (you can run it automatically if you want)::

        redis-server /usr/local/etc/redis.conf

Connect Redis to Flask, first let's some sample data::

        redis-cli
        redis 127.0.0.1:6379> set test "hello world"
        OK

Install python redis client::

        pip install redis

Change app.py and index.html.

Open a browser: http://localhost:5000/


Step 3: Hook up redis pub/sub
-----------------------------

Run::

        git checkout 2ceb7b71a512fd9581508d16629ccbba35797657

Subscribe to a redis channel [8]_::

        pip install gevent

Alter app.py, let's just print for the moment.

If you run using the flask built in wsgi server, you need the monkey patch. If
you run using gunicorn, then you won't need it.

Test::

        publish testing "awdawd 2"

Open a browser: http://localhost:5000/

Step 4: Hook up websockets to Python
------------------------------------

Run::

        git checkout 0041ba9135867d11f571b1524fe8ac29a24905d3

Communicate between Firefox (or Chrome) and python. Let's use Websockets [9]_.

We'll need a WebSocketWSGI handler::

        pip install gevent-websocket

Alter app.py, add in websocket handler, gevent.

Add in pace.js and jquery into static, print out websocket.

Test::

        publish testing "awdawd 2"

Open a browser: http://localhost:5000/

To run with gunicorn::

        gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" app:app


Step 5: Send in heart data
---------------------------

Run::

        git checkout 660df1be9c790a92b2fd55bc059a62955cbe3121

Send heart data. See ecg.py and ecg-data.csv.

Fire it up by running::

        python ecg.py

We can leave this running to pass in the data.

Note this is writing at one message per 7 ms.

Open a browser: http://localhost:5000/


Step 6: Add in a graph!
---------------------------

Run::

        git checkout f0e2fe01ba5592489bfaf521ee90355afb29bb49

Add in a graph, let's use smoothie [10]_.

Switch app.py to listen to ecg.

Most changes in index.html and pace.js

Note: try SmoothieChart({fps: 5});

Open a browser: http://localhost:5000/

Step 7: Flipping between subscriptions
--------------------------------------

Run::

        git checkout ec87b2d8e63a675b62b52740a6f2df728fac2eb2

Advanced-foo!

Let's add in flipping between subscriptions.

Open a browser: http://localhost:5000/


.. [1] http://pypi.python.org/pypi/virtualenv
.. [2] http://pypi.python.org/pypi/virtualenvwrapper
.. [3] You'll need to use this again each time you want to run this project,
       so try to remember this command.
.. [4] http://flask.pocoo.org/
.. [5] http://redis.io/
.. [6] http://mxcl.github.com/homebrew/
.. [7] You'll need to remember to run redis, if you don't set it up to run
       automatically, remember this command so that it you can remember how
       to run it.
.. [8] http://redis.io/commands#pubsub
.. [9] https://developer.mozilla.org/en/WebSockets
.. [10] http://smoothiecharts.org/
