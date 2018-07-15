import sqlite3
import matplotlib.dates as dates
import matplotlib.pyplot as plotter
from datetime import datetime
import twitterMain

twitterMain.twitterMain() #runs language analytics on all unanalysed stored data. TODO: move this functionality to real-time.

# sql structure: ( 0)rowID 1)CoinName, 2)netScore, 3)numberMentions, 4)wieghtedScore, 5)redordedDate, 6)recordedTime)
redditDbConnection = sqlite3.connect('redditData.db')
twitterDbConnection = sqlite3.connect('twitterData.db')
redditDbCursor = redditDbConnection.cursor()
twitterDbCursor = twitterDbConnection.cursor()

redditDbCursor.execute('select * from redditData')
allValues = redditDbCursor.fetchall()
numValues = len(allValues)

i = 0

while (i < numValues):
	print (allValues[i][0],repr(allValues[i][1]).ljust(16),repr(allValues[i][2]).ljust(6),repr(allValues[i][3]).ljust(6),repr(allValues[i][4]).ljust(6))
	i = i + 1
	if( i % 10 == 0): #prints headers every 10 lines
		print("\n")
		print("ID",repr("Coin Name").ljust(16), repr("Net.").ljust(6), repr("Ment.").ljust(6), repr("Weight.").ljust(6))
		print("\n")

def btcPlotter():
	k = 0
	btcWeightedScoreValues = list()
	btcROCValues = list()
	btcTimeValues = list()
	
	#data from reddit
	while (k < (numValues-10)):
		redditDbCursor.execute("select wieghtedScore from redditData where coinName is 'bitcoin' and rowID is ?", [k])
		btcScore = redditDbCursor.fetchone()
		if btcScore is not None:#handles bug giving 'type NoneObject' error. Ensures Score is an actual value
			btcWeightedScoreValues.append(btcScore[0])
		
		
		redditDbCursor.execute("select recordedTime from redditData where coinName is 'bitcoin' and rowID is ?", [k])
		btcTime = redditDbCursor.fetchone()
		if btcTime is not None:
			convertedTime =datetime.strptime((btcTime[0]),'%Y-%m-%d %H:%M:%S.%f') #converts string to dateTime for processing/readability
			btcTimeValues.append(convertedTime)
		k=k+10
		
	#rate of change calculation
	i = 10
	for i in range(0,(len(btcWeightedScoreValues))):
		btcROCValues.append((btcWeightedScoreValues[i]-btcWeightedScoreValues[i-10])/10) #slope calculation going 10 data points back

	#data from twitter
	
	btcTwitterWeightedValues = list()
	btcTwitterROCValues = list()
	btcTwitterTimeValues = list()
	
	twitterDbCursor.execute("select wieghtedScore from twitterData where coinName is 'bitcoin'")
	btcTwitValues = twitterDbCursor.fetchall()
	for k in range(0,len(btcTwitValues)):
		k=k*10
		twitterDbCursor.execute("select wieghtedScore from twitterData where coinName is 'bitcoin' and rowID is ?",[k])
		btcScore = twitterDbCursor.fetchone()
		if btcScore is not None:
			btcTwitterWeightedValues.append(btcScore[0])
			
		twitterDbCursor.execute("select recordedTime from twitterData where coinName is 'bitcoin' and rowID is ?",[k])
		btcTime = twitterDbCursor.fetchone()
		if btcTime is not None:
			convertedTime =datetime.strptime((btcTime[0]),'%Y-%m-%d %H:%M:%S.%f') #converts string to dateTime for processing/readability
			btcTwitterTimeValues.append(convertedTime)
	i = 10
	for i in range(0,(len(btcTwitterWeightedValues))):
		btcTwitterROCValues.append((btcTwitterWeightedValues[i]-btcTwitterWeightedValues[i-10])/10) #slope calculation going 10 data points back

	#plotting weighted values from reddit
	plotter.plot_date(btcTimeValues, btcWeightedScoreValues, '-', xdate = 'true')
	ax = plotter.axes()

	plotter.ylabel("Weighted Score")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Bitcoin \nWeighted Values(Reddit)")
	plotter.show()


	#plotting rate of change values from reddit
	plotter.plot_date(btcTimeValues, btcROCValues, '-')
	ax = plotter.axes()

	plotter.ylabel("Rate of Change")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Bitcoin \nRate of Change(Reddit)")
	plotter.show()
	
	#plotting weighted values from twitter
	plotter.plot_date(btcTwitterTimeValues, btcTwitterWeightedValues, '-')
	ax = plotter.axes()
	plotter.ylabel("Weighted Score")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Bitcoin \nWeighted Values(Twitter)")
	plotter.show()
	
	#plotting ROC values from twitter
	plotter.plot_date(btcTwitterTimeValues, btcTwitterROCValues, '-')
	ax = plotter.axes()
	plotter.ylabel("Rate of Change")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Bitcoin \nRate of Change(Twitter)")
	plotter.show()

def ethPlotter():
	k = 1 
	#data from reddit
	ethWeightedScoreValues = list()
	ethROCValues = list()
	ethTimeValues = list()
	ethNetScoreValues = list()
	while (k < (numValues-9)):
		redditDbCursor.execute("select wieghtedScore from redditData where coinName is 'ethereum' and rowID is ?", [k])
		ethScore = redditDbCursor.fetchone()
		if ethScore is not None:#handles bug giving 'type NoneObject' error. Ensures Score is an actual value
			ethWeightedScoreValues.append(ethScore[0])
		
		
		redditDbCursor.execute("select recordedTime from redditData where coinName is 'ethereum' and rowID is ?", [k])
		ethTime = redditDbCursor.fetchone()
		if ethTime is not None:
			convertedTime =datetime.strptime((ethTime[0]),'%Y-%m-%d %H:%M:%S.%f') #converts string to dateTime for processing/readability
			ethTimeValues.append(convertedTime)
		k=k+10
		
	#rate of change calculation
	i = 10

	for i in range(0,(len(ethWeightedScoreValues))):
		ethROCValues.append((ethWeightedScoreValues[i]-ethWeightedScoreValues[i-10])/10) #slope calculation going 10 data points back

		
	#data from twitter
	
	ethTwitterWeightedValues = list()
	ethTwitterROCValues = list()
	ethTwitterTimeValues = list()
	
	twitterDbCursor.execute("select wieghtedScore from twitterData where coinName is 'ethereum'")
	ethTwitValues = twitterDbCursor.fetchall()
	
	for k in range(0,len(ethTwitValues)):
		k = (k*10)+1
		twitterDbCursor.execute("select wieghtedScore from twitterData where coinName is 'ethereum' and rowID is ?",[k])
		ethScore = twitterDbCursor.fetchone()
		if ethScore is not None:
			ethTwitterWeightedValues.append(ethScore[0])
			
		twitterDbCursor.execute("select recordedTime from twitterData where coinName is 'ethereum' and rowID is ?",[k])
		ethTime = twitterDbCursor.fetchone()
		if ethTime is not None:
			convertedTime =datetime.strptime((ethTime[0]),'%Y-%m-%d %H:%M:%S.%f') #converts string to dateTime for processing/readability
			ethTwitterTimeValues.append(convertedTime)
	i = 10
	for i in range(0,(len(ethTwitterWeightedValues))):
		ethTwitterROCValues.append((ethTwitterWeightedValues[i]-ethTwitterWeightedValues[i-10])/10) #slope calculation going 10 data points back
		

	
	#plotting values from reddit	
	plotter.plot_date(ethTimeValues, ethWeightedScoreValues, '-', xdate = 'true')
	ax = plotter.axes()

	plotter.ylabel("Weighted Score")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ethereum \nWeighted Values(Reddit)")
	plotter.show()

	#ROC Values
	plotter.plot_date(ethTimeValues, ethROCValues, '-')
	ax = plotter.axes()

	plotter.ylabel("Rate of Change")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ethereum  \nRate of Change(Reddit)")
	plotter.show()
	
	
	#plotting values from twitter
	plotter.plot_date(ethTwitterTimeValues, ethTwitterWeightedValues, '-')
	ax = plotter.axes()
	plotter.ylabel("Weighted Score")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ethereum \nWeighted Values(Twitter)")
	plotter.show()
	
	
	#plotting ROC values from twitter
	plotter.plot_date(ethTwitterTimeValues, ethTwitterROCValues, '-')
	ax = plotter.axes()
	plotter.ylabel("Rate of Change")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ethereum \nRate of Change(Twitter)")
	plotter.show()

def xrpPlotter():
	k = 2 
	#data from reddit
	xrpWeightedScoreValues = list()
	xrpROCValues = list()
	xrpTimeValues = list()
	xrpNetScoreValues = list()
	while (k < (numValues-8)):
		redditDbCursor.execute("select wieghtedScore from redditData where coinName is 'ripple' and rowID is ?", [k])
		xrpScore = redditDbCursor.fetchone()
		if xrpScore is not None:#handles bug giving 'type NoneObject' error. Ensures Score is an actual value
			xrpWeightedScoreValues.append(xrpScore[0])
		
		
		redditDbCursor.execute("select recordedTime from redditData where coinName is 'ripple' and rowID is ?", [k])
		xrpTime = redditDbCursor.fetchone()
		if xrpTime is not None:
			convertedTime =datetime.strptime((xrpTime[0]),'%Y-%m-%d %H:%M:%S.%f') #converts string to dateTime for processing/readability
			xrpTimeValues.append(convertedTime)
		k=k+10
		
	#rate of change calculation
	i = 10

	for i in range(0,(len(xrpWeightedScoreValues))):
		xrpROCValues.append((xrpWeightedScoreValues[i]-xrpWeightedScoreValues[i-10])/10) #slope calculation going 10 data points back

		
	#data from twitter
	
	xrpTwitterWeightedValues = list()
	xrpTwitterROCValues = list()
	xrpTwitterTimeValues = list()
	
	twitterDbCursor.execute("select wieghtedScore from twitterData where coinName is 'ripple'")
	xrpTwitValues = twitterDbCursor.fetchall()
	for k in range(0,len(xrpTwitValues)):
		k = (k*10)+2
		twitterDbCursor.execute("select wieghtedScore from twitterData where coinName is 'ripple' and rowID is ?",[k])
		xrpScore = twitterDbCursor.fetchone()
		if xrpScore is not None:
			xrpTwitterWeightedValues.append(xrpScore[0])
			
		twitterDbCursor.execute("select recordedTime from twitterData where coinName is 'ripple' and rowID is ?",[k])
		xrpTime = twitterDbCursor.fetchone()
		if xrpTime is not None:
			convertedTime =datetime.strptime((xrpTime[0]),'%Y-%m-%d %H:%M:%S.%f') #converts string to dateTime for processing/readability
			xrpTwitterTimeValues.append(convertedTime)
	i = 10
	for i in range(0,(len(xrpTwitterWeightedValues))):
		xrpTwitterROCValues.append((xrpTwitterWeightedValues[i]-xrpTwitterWeightedValues[i-10])/10) #slope calculation going 10 data points back
		
		
	#plotting reddit values
	plotter.plot_date(xrpTimeValues, xrpWeightedScoreValues, '-', xdate = 'true')
	ax = plotter.axes()

	plotter.ylabel("Weighted Score")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ripple \nWeighted Values(Reddit)")
	plotter.show()


	#ROC values
	plotter.plot_date(xrpTimeValues, xrpROCValues, '-')
	ax = plotter.axes()

	plotter.ylabel("Rate of Change")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ripple  \nRate of Change(Reddit)")
	plotter.show()
	
	#plotting twitter Values
	plotter.plot_date(xrpTwitterTimeValues, xrpTwitterWeightedValues, '-')
	ax = plotter.axes()
	plotter.ylabel("Weighted Score")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ripple \nWeighted Values(Twitter)")
	plotter.show()
	
	
	#plotting ROC values from twitter
	plotter.plot_date(xrpTwitterTimeValues, xrpTwitterROCValues, '-')
	ax = plotter.axes()
	plotter.ylabel("Rate of Change")
	plotter.xlabel("Date")

	ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
	plotter.xticks(rotation=90)

	plotter.title("Market Attitudes on Ripple \nRate of Change(Twitter)")
	plotter.show()
	
	
	
	
btcPlotter()
ethPlotter()
xrpPlotter()



redditDbCursor.close()
redditDbConnection.commit()
redditDbConnection.close()

twitterDbCursor.close()
twitterDbConnection.commit()
twitterDbConnection.close()
