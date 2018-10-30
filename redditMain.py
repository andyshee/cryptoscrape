from Tally import tally
import praw
import sqlite3
import datetime

def wieghtedScore(netScore,mentions): #returns weighted score of coin to account for amount of discussion
	weightedScore = netScore / mentions
	return weightedScore
	
reddit = praw.Reddit(client_id = '' , 
						client_secret = '' ,
						username = '',
						password = ',
						user_agent = 'cryptoscrape') 

subreddit = reddit.subreddit('cryptocurrency')


coinList = ['bitcoin','ethereum','ripple','bitcoin cash','litecoin','eos','cardano','stellar','neo','iota'] #initialization of coin name lists
coinInitialList = ['btc','eth','xrp','bcash','ltc','eos','ada','xlm','neo','iota']

#database initialization stuff
testConnection = sqlite3.connect('redditData.db')
testCursor = testConnection.cursor()
testCursor.execute('''CREATE TABLE IF NOT EXISTS RedditData(rowID INTEGER, CoinName TEXT, netScore INTEGER, numberMentions INTEGER, wieghtedScore FLOAT, redordedDate DATE, recordedTime DATETIME)''')
testCursor.execute('select * from redditData')
allValues = testCursor.fetchall()
numValues = len(allValues)
testCursor.close()

scores = [0,0,0,0,0,0,0,0,0,0] #initialization of coin values list
coinMentions = [0,0,0,0,0,0,0,0,0,0]
weightedScores = [0,0,0,0,0,0,0,0,0,0]
mentionCounter = 0
counter = 0


if (numValues != 0): #tests to see if table is populated; if it is, values are set to most recent recorded values instead of array of zeroes
	position = 0
	for i in range((numValues-10),(numValues-1)):
				
		scores[position] = allValues[i][2]
		coinMentions[position] = allValues[i][3]
		weightedScores[position] = allValues[i][4]
		
		position = position + 1
		i = i + 1 
	counter = (allValues[numValues-1][0] + 1)

for comment in subreddit.stream.comments(): #retrieves reddit comments, this is a constant stream and not a 'traditional' for loop
	
	commentID = str(comment)
	commentText = reddit.comment(commentID).body
	normalizedCommentText = commentText.lower() #normalizes comment body to lowercase for analytics
		
	for i in range(0, len(coinList)): 
		if (tally(normalizedCommentText, coinList[i], coinInitialList[i]) != 0):
			
			change = tally(normalizedCommentText, coinList[i], coinInitialList[i])
			
			scores[i] = scores[i] + change #updates all scores and tallys
			coinMentions[i] = coinMentions[i] + 1
			#TODO: find a better algorithm to weight scores; this one becomes meaningless as number of mentions increases
			weightedScores[i] = wieghtedScore(scores[i],coinMentions[i])
			mentionCounter = mentionCounter + 1
			
			print ("\nCoin: " + coinList[i])
			print ("Score: " + str(scores[i]))
			print ("Weighted score: " + str(weightedScores[i]))
			print ("Number of mentions: " + str(coinMentions[i]))
			print ("Change: " + str(change))
			
			
	if (mentionCounter >= 5): #writes current data to database TODO: decrease writing frequency, find optimal number of data points for usable data
		#finding current date and time
		currentDate = datetime.date.today()
		currentTime = datetime.datetime.now()
		
		#database initialization stuff
		dbConnection = sqlite3.connect('redditData.db')
		dbCursor = dbConnection.cursor()
		
		
		print("\n\nWriting to file...\n")
		for i in range(0, len(coinList)): #writes all current data to SQL database
			dbCursor.execute('INSERT INTO redditData(rowID, CoinName, netScore, numberMentions, wieghtedScore, redordedDate, recordedTime) VALUES(?,?,?,?,?,?,?)' ,(counter, coinList[i], scores[i], coinMentions[i], weightedScores[i], currentDate, currentTime) )
			dbConnection.commit()
			counter = counter + 1
			if (dbCursor.rowcount != 1): #warning for error in file writing
				print('Error writing to .db file')

			
		dbCursor.close()
		mentionCounter = 0
