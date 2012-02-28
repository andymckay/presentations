import time
import redis
import csv

conn = redis.Redis()

filename = 'ecg-data.csv'
lines = []

read = csv.reader(open(filename))
lines = [l for l in read]

# We are doing True so that we'll have a continual flow of data from
# our sample data.
while True:
    for row in lines:
        time.sleep(0.007)
	# JavaScript time is in ms, so we need to increase Pythons time
        # to match JavaScript.
        data = [str(time.time() * 1000)] + row[1:]
        conn.publish('ecg', '|'.join(data))
