import time
import redis
import csv
import sys
import os

conn = redis.Redis()

filename = sys.argv[1]
lines = []

read = csv.reader(open(filename))
lines = [l for l in read]
nice = os.path.splitext(os.path.basename(filename))[0]


# We are doing True so that we'll have a continual flow of data from
# our sample data.
while True:
    try:
        conn.sadd('ecgs-keys', nice)
        for row in lines:
            time.sleep(0.007)
            # JavaScript time is in ms, so we need to increase Pythons time
            # to match JavaScript.
            data = [str(time.time() * 1000)] + row[1:]
            conn.publish('ecg-%s' % nice, '|'.join(data))
    except KeyboardInterrupt:
        conn.srem('ecgs-keys', nice)
        raise
