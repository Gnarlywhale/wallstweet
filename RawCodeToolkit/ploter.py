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

# ploter is a quick script used to graph results of data mining
# Each plot is highly customizable and specific to its dataset, so 
# more refinement and re-factoring should be done. 

import matplotlib
matplotlib.use('Agg')
import pylab
from plotBot import plotBot
from numpy import arange
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import datetime as DT
from matplotlib.dates import date2num, DayLocator, HourLocator, DateFormatter
print("start")
#create plots and extra axis on the right side
host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)
par1 = host.twinx()
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["right"].toggle(all=True)
#set labels
host.set_xlabel("Time Period")
host.set_ylabel("Tweet Ranking")

par1.set_ylabel("Stock Price")


#use the plotBot function to gather variable values
lines = plotBot().getLines(stock="ATVI")
x1 = list()
y1 = list()
for row in lines[0]:
	x1.append(date2num(row[0]))
	y1.append(row[1])
x2 = list()
y2 = list()
y3 = list()
for row in lines[1]:
	x2.append(date2num(row[0]))
	y2.append(row[1])
	y3.append(row[2])

#define everything to be plotted
p1 = par1.plot(x1, y1, label = 'Stock Price', linestyle='-', color = 'green')
p2 = host.plot(x2,y2, label = 'Tweet Sentiment Ranking',linestyle='-', color = 'red')
host.hlines(0.5, min(x2), max(x2), linestyle = '--', color = 'red') 
#p3 = host.bar(x2, y3, label = 'Time Period',align='center', color = 'blue', width = 0.1)
#adjust the scale to fit the data
host.set_ylim(0,1)
host.set_xlim(min(x2),max(x2))
par1.set_ylim(min(y1)-1,max(y1)+1)
#par2.set_ylim(0,1)
#create the fancy legend and title
box = host.get_position()
host.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
host.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3)
host.axis["left"].label.set_color('red')
par1.axis["right"].label.set_color('green')
host.xaxis.set_major_locator( DayLocator() )
host.xaxis.set_minor_locator( HourLocator(arange(0,25,6)) )
host.xaxis.set_major_formatter( DateFormatter('%m-%d') )

host.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
#par2.axis["right"].label.set_color('red')
pylab.title('Stock Price and Sentiment vs. Time for Microsoft')
pylab.savefig('foo.png')
print("done")

