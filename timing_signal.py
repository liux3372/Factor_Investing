#import trading
import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
from datetime import date
from astropy.table import Table
import scipy.stats
import os
import glob
from datetime_truncate import truncate
from collections import OrderedDict


def signal(path,looking_back_days):
	indexFrame=pd.read_csv(path,index_col=None,header=None,skiprows=[0,1,2,3],skipfooter=1,usecols=[0,4],engine='python')
	indexTime=indexFrame[indexFrame.columns[0]]
	indexClosing=indexFrame[indexFrame.columns[1]]
	allTradingdates=[datetime.strptime(x,' %Y/%m/%d')for x in indexTime]

	#truncate time column for defined total time span
	for m in range(len(allTradingdates)):
		if m!=0 and allTradingdates[m].year==startYear and allTradingdates[m].month==startMonth and allTradingdates[m-1].year==startYear and allTradingdates[m-1].month==startMonth-1:
			#print 'total start date'
			#print allTradingdates[m]
			startIndex=m
		# elif m!=0 and allTradingdates[m].year==endYear and allTradingdates[m].month==endMonth+1 and allTradingdates[m-1].year==endYear and allTradingdates[m-1].month==endMonth:
		# 	#print 'total end date'
		# 	#print allTradingdates[m]
		# 	endIndex=m
	#list slicing is [start,end), i.e. [2005.5.1,2014.5.1)
	usefulTradingDates=allTradingdates[startIndex:-1]
	usefulClosingPrices=indexClosing[startIndex:-1]
	closingPricesArr=np.asarray(usefulClosingPrices)

	movingAvg=[]
	signal=[]
	pos=0
	count=0

	for i in range(len(closingPricesArr)):
		if i<looking_back_days-1:
			movingAvg.append(-1)
			signal.append('N/A')
		else:
			#a=np.array([1,2,3,4,5])
			#a[0:6] would return array([1, 2, 3, 4, 5]) instead of indexOutOfBound exception 
			averagePrice=np.mean(closingPricesArr[i+1-looking_back_days:i+1])
			movingAvg.append(averagePrice)
			if pos==0 and closingPricesArr[i]>averagePrice:
				signal.append('Buy in the next trading day')
				pos=1
			elif pos==1 and closingPricesArr[i]<averagePrice:
				signal.append('Sell in the next trading day')
				pos=0
				count+=1
			elif i==len(closingPricesArr)-1 and pos==1:
				signal.append('Sell in the next trading day')
				pos=0
			else:
				signal.append('')


	return usefulTradingDates, usefulClosingPrices, movingAvg, signal, count




if __name__=='__main__':
	path='/Users/xinyuan/Desktop/codeForPaper/399300.csv'
	#inclusive variables
	startYear=2014
	endYear=2017
	startMonth=5
	endMonth=9
	looking_back_days=60
	usefulTradingDates, usefulClosingPrices, movingAvg, signal, count=signal(path,looking_back_days)
	print 'number of changing positions:%d'%(count)

	t=Table([usefulTradingDates, usefulClosingPrices, movingAvg, signal],names=('time','closing','moving average','signal'))
	t.write("sig.csv",format='csv')
















