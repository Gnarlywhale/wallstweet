'''
	wallstweet, February 9th, 2014
Data mining twitter with style. 

Copyright 2014 Riley Dawson, Kent Rasmussen, Chadwyck Goulet

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
__author__ = 'gnarlywhale'

import tweepy
import datetime
import calendar
import time
import nltk, MySQLdb
consumer_key = '4Mp6ti3sr21bVvzfYOCo3Q'
consumer_secret = 'JHjKExPm2RVtIXPdtklqZWfVDFfNq9ahF78OZ4zk'
access_token = '218005288-FoRxftZkDUxqtj4yBRlaubVVpE3rTa6TN4pxc2vk'
access_token_secret = 'INJfXEFUGqU0e7xXQ9zFEA73v1AaV30C6O0cOZACY4iSJ'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

db = MySQLdb.connect(host="localhost", user="wallstweet", db="wallstweet")
cur = db.cursor()

timespan = datetime.datetime.utcnow()
print(timespan)
#timespan = timespan - datetime.timedelta(seconds=30)
timespan = timespan - datetime.timedelta(days=30)


status = api.rate_limit_status()

# Determine if we're at our limit
limit = status['resources']['search']['/search/tweets']['remaining']
if(limit == 0):
    resetTime = int(status['resources']['search']['/search/tweets']['reset'])
    time.sleep(resetTime - calendar.timegm(datetime.datetime.utcnow().utctimetuple()) + 10)

for tweet in tweepy.Cursor(api.search, q="Activision", rpp=100, include_entities=True, lang="en", until='2014-02-08', since='2014-02-07').items():
    if(limit <= 5):
        status = api.rate_limit_status()
        limit = status['resources']['search']['/search/tweets']['remaining']
        if(limit <= 5):
            resetTime = int(status['resources']['search']['/search/tweets']['reset'])
            print("Sleeping for {0}!".format(resetTime - calendar.timegm(datetime.datetime.utcnow().utctimetuple()) + 10))
            time.sleep(resetTime - calendar.timegm(datetime.datetime.utcnow().utctimetuple()) + 10)

    huzzah = tweet.text.encode('ascii','ignore').replace('"', '\\"').replace('\\', '\\\\')

    cur.execute("INSERT IGNORE INTO tweet_dataset (id, text, time) VALUES (%s, %s, %s)", [tweet.id,huzzah,str(tweet.created_at)])
    db.commit()
    print("INSERTED: {2} {0} {1}".format(tweet.id,huzzah,str(tweet.created_at)))

    if tweet.created_at < timespan:
        break

    limit -= 1
    time.sleep(0.35)

cur.close()
