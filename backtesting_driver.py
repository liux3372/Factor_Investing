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


#path:(string)the current portfolio folder, which gets changed in __main__
#period(replaced):(int)the current time period 5,9,11 for May, Sep, Nov, which gets changed here
#timeVector:(datetime list) time span of current period
#initialFlag:(boolean)if the current period is the first period of all time, default is False, which gets changed in __main__
#lastFlag:(boolean)if the current period is the last period of all time, default is False, which gets changed in __main__
#prevClosing:<vector>the closing price of the previous portfolio, which is returned by last call of this function
#prevNumber:(int) number of stocks in previous portfolio, which is returned by last call of this function
#cash:(float) available cash to invest
#year:(int) current year of the portfolio, which gets changed in __main__
# def singlePortfolio(path,timeVector,initialFlag,lastFlag,prevClosing,prevNumber,cash,year,holdingAmt):
def singlePortfolio(path,timeVector,cash):
	#path=r'/Users/xinyuan/Desktop/codeForPaper/data/portfolio1'
	# print 'prevNumber'
	# print prevNumber
	together=path + "/*.csv"
	allFiles=glob.glob(together)
	currentNumber=len(allFiles)
	frame=pd.DataFrame()
	#frame=pd.read_csv(r"/Users/xinyuan/Desktop/codeForPaper/data/20040501/000001.csv",index_col=None,header=None,skiprows=[0,1],skipfooter=1,usecols=[0,1,4],engine='python')
	frame=pd.concat((pd.read_csv(f,index_col=None,header=None,skiprows=[0,1],skipfooter=1,usecols=[0,1,4],engine='python') for f in allFiles))
	strDates=frame[frame.columns[0]]
	opening=frame[frame.columns[1]]
	closing=frame[frame.columns[2]]

	dates=[datetime.strptime(x,'%Y/%m/%d')for x in strDates]
	#yearMonth=pd.to_datetime(strDates).dt.to_period('M').values
	# currentOpening=np.array([])
	# currentClosing=np.array([])

	#starting index of each stock
	stockStart=[]
	for h in range(len(dates)):
		if h==0:
			stockStart.append(h)
		elif dates[h-1].year>dates[h].year:
			stockStart.append(h)



	allocationNum=float(cash)/currentNumber
	#vector for remaining cash of each stock
	allocationVector=np.empty(currentNumber); allocationVector.fill(allocationNum)
	buyFlags=np.empty(currentNumber); buyFlags.fill(0)

	#lots vector:number of 100 shares of each stock
	amountVector=np.empty(currentNumber); amountVector.fill(0)
	#vector for asset of each stock
	assetVector=np.empty(currentNumber); assetVector.fill(allocationNum)
	#vector for daily total asset
	dailyTotalAsset=np.empty(len(timeVector)); dailyTotalAsset.fill(0)
	#closing price so far for each stock(used for asset calculation)
	closingSofar=np.empty(currentNumber); amountVector.fill(0)

	bid=0
	endIndex=0

	for t in range(len(timeVector)):
		today=timeVector[t]
		#if it is not the last day
		if t!=len(timeVector)-1:
			#iterate through each stock
			for i in range(currentNumber):
				#buy stocks if it has not been bought
				if buyFlags[i]==0:
					if i==currentNumber-1:
						endIndex=len(dates)
					else:
						endIndex=stockStart[i+1]
					# print "stockStart[%d]:%d" % (i,stockStart[i])
					# print "endIndex:%d" % endIndex
					for k in range(stockStart[i],endIndex):
						#if the stock is trading today
						if dates[k]==today:
							#print "k:%d" %k
							bid=opening[k:k+1]
							closingSofar[i]=closing[k:k+1]
							#print "bid:%.6f" % (bid)
							if ((pd.to_numeric(bid)>0).bool()):
								amountVector[i]=np.floor(float(allocationVector[i])/(100*bid))
							else:
								amountVector[i]=0
							#print "amountVector[%d]:%.6f" % (i,amountVector[i])
							allocationVector[i]=allocationVector[i]-np.sum(amountVector[i]*100*bid)
							#print "allocationVector[%d]:%.6f" % (i,allocationVector[i])
							buyFlags[i]=1
							if amountVector[i]>0 and closingSofar[i]>0:
								assetVector[i]=amountVector[i]*100*closingSofar[i]
							#assetVector stays the same, so below can be neglected
							#assetVector[i]=allocationNum
				#get daily asset for stocks that have already bought:buyFlags[i]!=0
				else:
					if i==currentNumber-1:
						endIndex=len(dates)
					else:
						endIndex=stockStart[i+1]
					for kk in range(stockStart[i],endIndex):
						if dates[kk]==today:
							closingSofar[i]=closing[kk:kk+1]
					if amountVector[i]>0 and closingSofar[i]>0:
						assetVector[i]=amountVector[i]*100*closingSofar[i]
					#print "assetVector[%d]:%.6f" % (i,assetVector[i])
		#dailyTotalAsset[t]=np.sum(assetVector)
		#case for last day of the period to sell all the stocks
		else:
			for ii in range(currentNumber):
				if ii==currentNumber-1:
					endIndex=len(dates)
				else:
					endIndex=stockStart[ii+1]
				for kkk in range(stockStart[ii],endIndex):
					#if the stock is trading today
					if dates[kkk]==today:
						closingSofar[i]=closing[kkk:kkk+1]
			assetVector[i]=allocationVector[i]+amountVector[i]*100*closingSofar[i]
		dailyTotalAsset[t]=np.sum(assetVector)	


	return dailyTotalAsset



	#only used if all the stocks can be trading on all the available trading days
	# for i in range(len(dates)):
	# 	if dates[i]==timeVector[0]:
	# 		#print dates[i]
	# 		#print timeVector[0]
	# 		currentOpening=np.append(currentOpening,opening[i:i+1])
	# 	elif dates[i]==timeVector[-1]:
	# 		#print dates[i]
	# 		#print timeVector[-1]
	# 		currentClosing=np.append(currentClosing,closing[i:i+1])

if __name__=="__main__":
	# for root, dirs, files in os.walk('/Users/xinyuan/Desktop/codeForPaper/data/'):
	# 	print root
	# 	print dirs

	#!!! dataSrc should be the one subdirectory inside of pwd
	#dataSrc='/Users/xinyuan/Desktop/codeForPaper/data/'
	print 'pay attention to data path'
	dataSrc='/Users/xinyuan/Desktop/codeForPaper/Step1_validation_of_four_factors/XJL_data/'
	initialFlag=False
	lastFlag=False
	prevClosing=[]
	currentClosing=[]
	prevNumber=0
	currentNumber=0
	cashRemain=0
	initialCash=100000000

	assetNum=0

	#inclusive variables
	startYear=2005
	endYear=2014
	startMonth=5
	endMonth=4

	holdingAmt=np.array([])

	currentYear=0
	#for output
	time=[]
	asset=[]
	netValue=[]

	#!!! change pwd into dataSrc
	os.chdir(dataSrc)
	dirList=next(os.walk('.'))[1]
	#print dirList
	dirDates=[datetime.strptime(p,'%Y%m%d')for p in dirList]
	dirDates=sorted(dirDates)

	#read index for available trading days
	indexPath='/Users/xinyuan/Desktop/codeForPaper/000001index.csv'
	indexFrame=pd.read_csv(indexPath,index_col=None,header=None,skiprows=[0,1],skipfooter=1,usecols=[0],engine='python')
	indexTime=indexFrame[indexFrame.columns[0]]
	allTradingdates=[datetime.strptime(x,'%Y/%m/%d')for x in indexTime]

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

	# for h in range(len(monthIndexList)):
	# 	print usefulTradingDates[monthIndexList[h]]
	# for key in sorted(monthIndexList.keys()):
	# 	print key,monthIndexList[key]

#iterate through each dir below
#---------------------------------------------------------
	for k in range(len(dirDates)):
		

		#print 'period:'+str(period)
		#e.g. 20040501 in string
		currentYear=dirDates[k].year
		ymd=str(dirDates[k].year)+str(dirDates[k].month)+str(dirDates[k].day)
		#print ymd
		#print dirDates[k].date
		#!!!attention to match folder names
		path=dataSrc+dirList[k]
		print 'path:'+path
		#number of csv files(without subdirs) in current portfolio folder
		together=path + "/*.csv"
		allFiles=glob.glob(together)
		prevNumber=len(allFiles)

		#number of all files(without subdirs) in current portfolio folder
		#prevNumber=len(next(os.walk(path))[2])
		#print 'prevNumber:'+str(prevNumber)
		# print next(os.walk(path))[2]

		#start month, which is actually startMonth
		if k==0:
			period=dirDates[k].month

		#start and end month of each period,e.g. [2005.5.1,2014.5.1) semi-inclusive
		periodStart=dirDates[k]
		
		if k==len(dirDates)-1:
			#last date is first trading day in 2014.5, exlusive
			periodEnd=usefulTradingDates[-1]
		else:
			periodEnd=dirDates[k+1]

		#generate time span for each period
		timeVectorBegin=sortedMonth.keys()[sortedMonth.values().index(periodStart)]
		timeVectorEnd=sortedMonth.keys()[sortedMonth.values().index(periodEnd)]
		timeVector=usefulTradingDates[timeVectorBegin:timeVectorEnd]

		#print k
		#print timeVector
		#-------------------------------------------------------------
		time.append(timeVector)
		#-------------------------------------------------------------
		if k==0:
			cash=initialCash
		else:
			cash=assetNum
		assetVector=singlePortfolio(path,timeVector,cash)
		assetNum=assetVector[-1]
		#-------------------------------------------------------------
		asset.append(assetVector.tolist())
		netValueVector=assetVector/float(initialCash)
		netValue.append(netValueVector.tolist())
		#-------------------------------------------------------------


	time=[val for sublist in time for val in sublist]
	asset=[val for sublist in asset for val in sublist]
	netValue=[val for sublist in netValue for val in sublist]

	t=Table([time,asset,netValue],names=('time','asset','netValue'))
	#t=Table([time,asset,netValue])
	t.write("result.csv",format='csv')





