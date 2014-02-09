import nltk, MySQLdb

class SentimentData:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", user="wallstweet", db="wallstweet")
		cur = self.db.cursor()
		cur.execute("SELECT text, rating FROM sentiment_dataset LIMIT 500")
		
		words = []
		data = []
		for (text, rating) in cur.fetchall():
			# Add to the list of data
			words_filtered = [e.lower() for e in text.split() if len(e) >= 3]
			data.append((words_filtered, rating))
		
			# Add all words in the data to all of the words
			words.extend(words_filtered)
		cur.close()
		
		self.word_features = nltk.FreqDist(words).keys()
		training_set = nltk.classify.apply_features(_sentiment_features, data)
		self.classifier = nltk.NaiveBayesClassifier.train(training_set)
		
	def _sentiment_features(string):
		words = set(string.split())
		features = {}
		for word in self.word_features:
			features['contains(%s)' % word] = (word in string_words)
		return features
		
	def classify_data(self, string):
		return self.classifier.classify(self._sentiment_features(string))