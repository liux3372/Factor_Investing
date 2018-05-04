#!/usr/bin/env python
# -*- coding: utf-8 -*- 
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
from shutil import copy



#env='/Users/xinyuan/Desktop/codeForPaper/' for this code file
if __name__=="__main__":
	#read index for available trading days
	env='/Users/xinyuan/Desktop/codeForPaper/'
	indexPath=env+'000001index.csv'
	indexFrame=pd.read_csv(indexPath,index_col=None,header=None,skiprows=[0,1],skipfooter=1,usecols=[0],engine='python')
	indexTime=indexFrame[indexFrame.columns[0]]
	allTradingdates=[datetime.strptime(x,'%Y/%m/%d')for x in indexTime]

	startYear=2005
	endYear=2014
	startMonth=5
	endMonth=4

	#truncate time column for defined total time span
	for m in range(len(allTradingdates)):
		if m!=0 and allTradingdates[m].year==startYear and allTradingdates[m].month==startMonth and allTradingdates[m-1].year==startYear and allTradingdates[m-1].month==startMonth-1:
			#print 'total start date'
			#print allTradingdates[m]
			startIndex=m
		elif m!=0 and allTradingdates[m].year==endYear and allTradingdates[m].month==endMonth+1 and allTradingdates[m-1].year==endYear and allTradingdates[m-1].month==endMonth:
			#print 'total end date'
			#print allTradingdates[m]
			endIndex=m
	#list slicing is [start,end), i.e. [2005.5.1,2014.5.1)
	usefulTradingDates=allTradingdates[startIndex:endIndex+1]
	
	#2014-04-30 00:00:00
	#print usefulTradingDates[-1]

	
	#OrderedDict of {index: start of every month}
	monthIndexList={}
	for n in range(len(usefulTradingDates)):
		if n==0:
			monthIndexList[n]=usefulTradingDates[n]
		elif usefulTradingDates[n].month != usefulTradingDates[n-1].month:
			# monthIndexList.append(n,usefulTradingDates[n])
			monthIndexList[n]=usefulTradingDates[n]

	sortedMonth=OrderedDict(sorted(monthIndexList.items(),key=lambda t:t[0]))

	#should be (2014-2005)*12+1=109
	#print "length: %d" % len(sortedMonth)
	#OrderedDict([(0, datetime.datetime(2005, 5, 9, 0, 0)), (17, datetime.datetime(2005, 6, 1, 0, 0)),...,(2184, datetime.datetime(2014, 5, 5, 0, 0))])
	#print sortedMonth

	# timeVectorBegin=sortedMonth.keys()[sortedMonth.values().index(periodStart)]
	# timeVectorEnd=sortedMonth.keys()[sortedMonth.values().index(periodEnd)]
	# timeVector=usefulTradingDates[timeVectorBegin:timeVectorEnd]

	# #print k
	# print timeVector
	path='/Users/xinyuan/Desktop/codeForPaper/raw_data/PEG/pool'
	print 'path of pool:%s'%(path)
	together=path + "/*.xlsx"
	allFiles=glob.glob(together)
	#currentNumber=len(allFiles)
	frame=pd.DataFrame()

	if not os.path.exists('data'):
		os.makedirs('data')

	for f in allFiles:
		fileName=os.path.basename(f)
		prefix='R_'
		suffix=".xlsx"
		temp=fileName.replace(prefix,'')
		#folderName='data/'+temp.replace(suffix,'')

		#e.g. 20050501 and manually set to the first trading day
		periodYMD=temp.replace(suffix,'')
		periodDatetime=datetime.strptime(periodYMD,'%Y%m%d')
		newDate=periodDatetime

		for i in range(len(usefulTradingDates)):
			#periodDatetime.month can only be 5,9 or 11
			if i!=0 and usefulTradingDates[i].year==periodDatetime.year and usefulTradingDates[i].month==periodDatetime.month and usefulTradingDates[i-1].month==periodDatetime.month-1:
				#print usefulTradingDates[i]
				newDate=periodDatetime.replace(day=usefulTradingDates[i].day)
				#print newDate
			#special case for i==0
			elif periodDatetime.year==2005 and periodDatetime.month==5:
				newDate=periodDatetime.replace(day=usefulTradingDates[0].day)


		folderName='data/'+newDate.strftime('%Y%m%d')

		#print folderName
		if not os.path.exists(folderName):
			os.makedirs(folderName)

		

		dataFrame = pd.read_excel(f)
		stockCode=dataFrame[u'证券代码'].values
		shanghai='.SH'
		shenzhen='.SZ'

		marketPath=env+'market_split_adjusted_backward/'

		for code in stockCode:
			if shanghai in code:
				code=code.replace(shanghai,'')
				#print code
				src=marketPath+str(code)+'.csv'
				dst=env+folderName
				copy(src,dst)
			elif shenzhen in code:
				code=code.replace(shenzhen,'')
				#print code
				src=marketPath+str(code)+'.csv'
				dst=env+folderName
				copy(src,dst)
			else:
				print 'error in stock code %s' % (code)

		#print stockCode
		#break































