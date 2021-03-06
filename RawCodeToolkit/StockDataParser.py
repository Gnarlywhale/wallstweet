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

# The StockDataParser mines google finance for the stock price data.
# It can be initialized with the chosen stock symbol, exchange, time period (days),
# and time interval (seconds)
__author__ = 'Riley'
import urllib
import nltk, MySQLdb
import datetime
import time
class StockDataParser:
    def __init__(self,stock="MSFT",exchange="NASDAQ",period=30,interval=1800):
		# Set url query
        url_string = "http://www.google.com/finance/getprices?q={0}&x={1}&p={2}d&i={3}&f=d,o,h,l,c".\
            format(stock.upper(),exchange.upper(), period, interval)
        
		
        print(url_string)
        response = urllib.urlopen(url_string).readlines()
      
		# Skip first 6 lines)
        offset = int(response[6][16:])

		# Initialize base Time (starting time of period)
        baseTime = 0
        
		# Connect to database
        db = MySQLdb.connect(host="localhost", user="wallstweet", db="wallstweet")
        cur = db.cursor()
		# Set time format
        f = '%Y-%m-%d %H:%M:%S'

		# Step through returned rows of price over time data
        for idx in range(7,len(response)):
            row = response[idx].split(",")
            if row[0][0] == 'a':
                baseTime = int(row[0][1:])
                priceTime = baseTime+(int(offset)*60)
            else:
                priceTime = baseTime+(int(row[0])*interval)+(int(offset)*60)
            price = float(row[1])

            print(str(priceTime)+" "+str(price))

			# Add data to database
            cur.execute("INSERT INTO stock_dataset  (id, time, price) VALUES (\"{0}\",\"{1}\",{2})".format(stock,str(datetime.datetime.utcfromtimestamp(priceTime)),
                        price))

            print ("INSERT INTO stock_dataset  (id, time, price) VALUES ({0},{1},{2})".format(stock,priceTime,
                        price))



        db.commit()
        cur.close()
            #print(row)
            #c.writerow(row)

        #print("done")
# Set stock and other flags
something = StockDataParser(stock="ATVI",period="7")
