import nltk, MySQLdb

class SentimentData:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", user="wallstweet", db="wallstweet")
		cur = self.db.cursor()
		cur.execute("SELECT text, rating FROM sentiment_dataset")
		
		self.words = []
		self.data = []
		for (text, rating) in cur.fetchall():
			# Add to the list of data
			words_filtered = [e.lower() for e in text.split() if len(e) >= 3]
			self.data.append((words_filtered, rating))
		
			# Add all words in the data to all of the words
			for word in words_filtered:
				words.append(word)
		cur.close()
		
		self.word_features = nltk.FreqDist(wordlist).keys()
		self.training_set = nltk.classify.apply_features(_extract_features, tweets)
		self.classifier = nltk.NaiveBayesClassifier.train(training_set)
		
	def _extract_features(self, string):
		string_words = set(string)
		features = {}
		for word in self.word_features:
			features['contains(%s)' % word] = (word in string_words)
		return features
		
	def classify_data(self, string):
		return self.classifier.classify(_extract_features(string))