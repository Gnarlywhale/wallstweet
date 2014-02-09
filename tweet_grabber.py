#!/usr/bin/python2.7

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

import json, time
import nltk, tweepy
from wallstweet import database

# Creates a ranking of the top words used most often
def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features
	
db = database()

all_words = []
tweets = []
for (text, rating) in db.get_sentiment_data(10):
	# Add to tweets list
	words_filtered = [word for word in text.split() if len(word) >= 3]
	tweets.append((words_filtered, rating))
	
	# Add tweet words to list of all words
	all_words.extend(words_filtered)

wordlist = nltk.FreqDist(all_words)
word_features = list(wordlist.keys())

# Creates a list of words that are contained in this tweet
def extract_features(tweet):
	tweet_words = set(tweet)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in tweet_words)
	return features

# Create our training set
training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

# Get configuration
config_file = open("config.json", 'r')
config_json = json.load(config_file)
twitter_config = config_json['twitter_config']
stocks = config_json['stocks']
config_file.close()

# Mine tweets
auth = tweepy.OAuthHandler(twitter_config['api'], twitter_config['api_secret'])
auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
api = tweepy.API(auth)

status = api.rate_limit_status()['resources']['search']['/search/tweets']
# Determine if we're at our limit, even before we start
limit = status['remaining']
if(limit == 0):
	#resetTime = int(status['reset'])
	reset_time = status['reset']
	current_time = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
	time.sleep(reset_time - current_time - 10) # sleep an extra 10 seconds, just to be safe

while True:
	# Iterate through each stock ID
	for stockID, stockConfig in stocks.iteritems():
		# Generate search terms for twitter
		search = ""
		has_term = False
		aliases = []
		for stock in stockConfig['aliases']:
			aliases.append(stock)
			if(has_term):
				search = search + " OR "
			has_term = True
			search = search + "\"" + stock + "\""
			
		last_id = db.get_last_tweet_id(aliases)
		print("MaxID:", last_id)
		print("Search:", search)
		for tweet in tweepy.Cursor(api.search, q=search, rpp=100, include_entities=True, lang="en", from_id=last_id).items():
			if(limit <= 5):
				status = api.rate_limit_status()['resources']['search']['/search/tweets']
				limit = status['remaining']
				if(limit <= 5):
					reset_time = status['reset']
					current_time = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
					print("Sleeping for {0}!".format(reset_time - current_time - 10))
					time.sleep(reset_time - current_time - 10) # sleep an extra 10 seconds, just to be safe
			
			text = tweet.text.encode('ascii','ignore')
			polarity = classifier.prob_classify(extract_features(text.split())).prob('positive')
			db.add_tweet(tweet.id, text, tweet.created_at, polarity)
			print("Added {0}! {1} {2}".format(tweet.id, tweet.created_at, text))
			time.sleep(0.5)
			if(last_id >= tweet.id):
				print("Reached last id! Sleeping 60s!")
				time.sleep(60)
				break;
	print("Went through all stocks! Sleeping 60s!")
	time.sleep(60)