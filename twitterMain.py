def twitterMain():
	import sqlite3
	import datetime
	from Tally import tally

	coinList = ['bitcoin','ethereum','ripple','bitcoin cash','litecoin','eos','cardano','stellar','neo','iota']
	coinInitialList = ['btc','eth','xrp','bcash','ltc','eos','ada','xlm','neo','iota']
	scores = [0,0,0,0,0,0,0,0,0,0] #initialization of coin values list
	coinMentions = [0,0,0,0,0,0,0,0,0,0]
	weightedScore = [0,0,0,0,0,0,0,0,0,0]
	mentionCounter = 0
	counter = 0

	def calcWieghtedScore(netScore,mentions): #returns weighted score of coin to account for amount of discussion
		weightedScore = netScore / mentions
		return weightedScore

		
	#tests to see if table is populated; if it is, values are set to most recent recorded values instead of array of zeroes
	testConnection = sqlite3.connect('twitterData.db')
	testCursor = testConnection.cursor()
	testCursor.execute('CREATE TABLE IF NOT EXISTS twitterData(rowID INTEGER, CoinName TEXT, netScore INTEGER, numberMentions INTEGER, wieghtedScore FLOAT, redordedDate DATE, recordedTime DATETIME)')
	testCursor.execute('select * from twitterData')
	allValues = testCursor.fetchall()
	numValues = len(allValues)
	testCursor.close()
	if (numValues != 0): 
		position = 0
		for i in range((numValues-10),(numValues-1)):
			scores[position] = allValues[i][2]
			coinMentions[position] = allValues[i][3]
			weightedScore[position] = allValues[i][4]
			
			position = position + 1
			i = i + 1 
		counter = (allValues[numValues-1][0] + 1)
		
	#populates arrays with raw data from generator
	textList = list()
	datesList = list()

	rawConn = sqlite3.connect('twitterRawData.db')
	rawCursor = rawConn.cursor()
	
	rawCursor.execute('select body from twitterRawData')
	allText = rawCursor.fetchall()
	rawCursor.execute('select recordedTime from twitterRawData')
	allDates = rawCursor.fetchall()
	rawCursor.execute('select analyzed from twitterRawData')
	analyzed = rawCursor.fetchall()
	analyzedCounter=0

	for i in range (0, (len(allText))):
		if (analyzed[i][0] == 0):
			textList.append(allText[i][0]) #[0] selects first element from tuple of length 1
			datesList.append(allDates[i][0])
		else:
			analyzedCounter = analyzedCounter + 1
	rawCursor.execute('select analyzed from twitterRawData')
	analyzed = rawCursor.fetchall()

	for k, bodyText in enumerate(textList): #creates index 'k' to be used to check if row has been analyzed, provides bodyText object to next loop
		for i in range (0,len(coinList)):
			if(tally(bodyText,coinList[i],coinInitialList[i]) != 0 and analyzed[(analyzedCounter+k)][0] == 0):
				scores[i] = scores[i] + tally(bodyText, coinList[i], coinInitialList[i])
				coinMentions[i] = coinMentions[i] + 1
				weightedScore[i] = calcWieghtedScore(scores[i],coinMentions[i])
				mentionCounter = mentionCounter + 1	 
				
				print ("\nCoin: " + coinList[i])
				print ("Score: " + str(scores[i]))
				print ("Weighted score: " + str(weightedScore[i]))
				print ("Number of mentions: " + str(coinMentions[i]))
				
				if (mentionCounter >= 5): #writes current data to database TODO: decrease writing frequency, find optimal number of data points for usable data
					#finding current date and time
					currentDate = datetime.date.today()
					currentTime = datetime.datetime.now()
					
					#database initialization stuff
					dbConnection = sqlite3.connect('twitterData.db')
					dbCursor = dbConnection.cursor()

					print("\n\nWriting to file...\n")
					for i in range(0, len(coinList)): #writes all current data to SQL database
						dbCursor.execute('INSERT INTO twitterData(rowID, CoinName, netScore, numberMentions, wieghtedScore, redordedDate, recordedTime) VALUES(?,?,?,?,?,?,?)' ,(counter, coinList[i], scores[i], coinMentions[i], weightedScore[i], currentDate, datesList[k]) )
						dbConnection.commit()
						counter = counter + 1
						if (dbCursor.rowcount != 1): #warning for error in file writing
							print('Error writing to .db file')
					mentionCounter = 0
					dbCursor.close()
				
	rawCursor.execute('UPDATE twitterRawData SET analyzed = 1') 
	rawCursor.close()
	rawConn.commit()
	rawConn.close()
	
twitterMain()