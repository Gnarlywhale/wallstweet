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

import datetime, json

# Get configuration
config_file = open("config.json", 'r')
config_json = json.load(config_file)
stocks = config_json['stocks']
config_file.close()

#while(True):
	current_time = datetime.datetime.utcnow()
	
	# TODO: sleep until next stock quote
	
	# TODO: For each stock
		
		# Download latest quote and add to database