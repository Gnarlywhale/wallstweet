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

__author__ = 'Riley'
import nltk, MySQLdb
import datetime

class plotBot:
	def getLines(self,stock="MSFT",exchange="NASDAQ",interval=30,startTime=None,endTime=None):
		if endTime == None:
			endTime = datetime.datetime.utcnow()
		if startTime == None:
			startTime = endTime - datetime.timedelta(days=3)
		print startTime
		print endTime		
		db = MySQLdb.connect(host="localhost",user="wallstweet", db="wallstweet")
		cur1 = db.cursor()
		lines = list()
		lines.append(list())
		lines.append(list())
		lines.append(list())

		cur1.execute("SELECT ROUND(UNIX_TIMESTAMP(time)/(%s * 60)) AS timeinterval, AVG(price), MIN(time) FROM stock_dataset WHERE time >= %s and time <= %s and id=%s GROUP BY timeinterval", [interval, str(startTime), str(endTime), stock])

		stockRows = cur1.fetchall()
		print(len(stockRows))
		for row in stockRows:
			lines[0].append([row[2],row[1]]) 

		cur2 = db.cursor()


		if(stock == "MSFT"):
			company = "@Microsoft"
		if(stock == "YUM"):
			company = "Yum Brands"

		if(stock == "ATVI"):
			company = "Activision"

		cur2.execute("SELECT ROUND(UNIX_TIMESTAMP(time)/(%s * 60)) AS timeinterval, AVG(polarity), MIN(time), COUNT(*) FROM tweet_dataset WHERE time >= %s AND time <= %s AND text LIKE %s GROUP BY timeinterval",[interval, str(startTime), str(endTime), "%" + company + "%"])
	
		tweetRows = cur2.fetchall()

		for row in tweetRows:
			lines[1].append([row[2],row[1],row[3]])

		print(len(tweetRows))

#		for row in tweetRows:
#			print(row)
		return lines
#fun= plotBot()

lines = plotBot().getLines()
x = list()
y1 = list()
for row in lines[0]:
#	print(str(row[0])+" "+str(row[1]))		
	x.append(row[0])
	y1.append(row[1])
#print(len(x))
#print(len(y1))

