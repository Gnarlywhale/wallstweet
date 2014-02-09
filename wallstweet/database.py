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

import json, MySQLdb

class database:
	def __init__(self, config="config.json"):
		# Get configuration
		config_file = open(config, 'r')
		database_config = json.load(config_file)['database_config']
		config_file.close()
		
		# Connect to database
		self.db = MySQLdb.connect(host=database_config['host'], user=database_config['username'], db=database_config['database'], passwd=database_config['password'])
		return
		
	def get_sentiment_data(self, limit=2500):
		# Get & return sentiment data from the database
		cursor = self.db.cursor()
		cursor.execute("SELECT LOWER(text), rating FROM sentiment_dataset LIMIT %s", [limit])
		results = cursor.fetchall()
		cursor.close()
		return results
		
	def get_last_tweet_id(self, searchterms=None):
		cursor = self.db.cursor()
		sql = "SELECT MAX(id) FROM tweet_dataset"
		if(searchterms == None):
			print(sql)
			cursor.execute(sql)
		else:
			variables = 0;
			converted = []
			for term in searchterms:
				converted.append("%" + term + "%")
				if(variables > 0):
					sql = sql + " OR"
				else:
					sql = sql + " WHERE"
				
				sql = sql + " text LIKE %s"
				variables = variables + 1
			
			print(converted)
			print(sql)
			cursor.execute(sql, converted)
			return cursor.fetchone()[0]
			
	def add_tweet(self, id, text, time, polarity=None):
		cursor = self.db.cursor()
		cursor.execute("INSERT IGNORE INTO tweet_dataset (id, text, time, polarity) VALUES(%s, %s, %s, %s)", [id, text, time, polarity])
		self.db.commit()
		cursor.close()
