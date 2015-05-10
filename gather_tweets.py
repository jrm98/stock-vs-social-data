#!/usr/bin/python

# pulls twitter data from specified user streams
from __future__ import print_function
import urllib2, time, threading, oauth, datetime, time
from twitter import *
import logging
logging.basicConfig(filename='log/log.txt',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

# load our API credentials 
config = {}
execfile("config.py", config)

def _warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)
def _error(*objs):
    print("ERROR: ", *objs, file=sys.stderr)

# create twitter API object
twitter = Twitter(
		auth = OAuth(config['access_key'], 
			config['access_secret'], 
			config['consumer_key'], 
			config['consumer_secret']))

traders = config['traders']
last_req = datetime.datetime.today()

logging.debug(' INITIALIZATION DONE')

for user in traders:
	# total number of tweets to pull for each user
	max_tweets = 9000
	limit = datetime.datetime(2015, 1, 28)
	current = datetime.datetime.today()

	try:
		f = open('data/tweets/'+user+'.txt','w')
		f.seek(0)

		last_id = 0
		i = 0
		while i < max_tweets and limit < current:
			logging.debug('entering new iteration for '+user)
			logging.debug('checking rate limiting...')
			# rate limiting
			while (datetime.datetime.today() - last_req).total_seconds() < 5:
				time.sleep(2)

			logging.debug('...done')
			if last_id != 0:
				results = twitter.statuses.user_timeline(screen_name=user, 
					count=200,
					max_id=last_id)
			else:
				results = twitter.statuses.user_timeline(screen_name=user, 
					count=200)

			tstr = (results[len(results)-1]['created_at'])[0:19] + \
			(results[len(results)-1]['created_at'])[25:]

			tstr = tstr.strip()

			logging.debug('tstr = '+tstr)

			current = datetime.datetime.strptime(tstr, 
				"%a %b %d %H:%M:%S %Y")
			last_id = int(results[len(results) - 1]['id'])

			# display in terminal
			for status in results:
				print("(%s) %s" % (status['created_at'], status['text']))


			# save to file
			for status in results:
				f.write( "(%s) " % status['created_at']) 
				f.write(status['text'].encode("utf-8"))
				f.write("\n")

			i += 200

		f.truncate()
		f.close()
	except IOError:
		_error('file '+'data/tweets/'+user+'.txt'+' could not be written to')

logging.debug(' PROGRAM COMPLETED')
