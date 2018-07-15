from tweepy import API
from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
from Tally import tally
import sqlite3
import datetime

#twitter set up	
consumer_key = 'jAk3IZ4XsjqcyDVNG3qfNqWe4' 
consumer_secret = 'OM2xxzddkk9c7Y5XrVCXZHkxS8DkTBRlYXKqVqsuROhkA36utH'
access_token = '1864112844-FZixJgbqGW3wB6G0Y4tu8mdftHF1MWWwTmilInZ'
access_secret = 'buSeQMMwSZMvPXvULEOaGvZzYAIsdUfR7eqD3zroOOYQa'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = API(auth)

coinList = ['bitcoin','ethereum','ripple','bitcoin cash','litecoin','eos','ripple','cardano','neo','iota']
coinInitialList = ['btc','eth','xrp','bcash','ltc','eos','ada','xlm','neo','iota']
trackingList = ["$BTC","$ETH","$XRP","$BCASH","$LTC","$EOS","$ADA","$XLM","$NEO","$IOTA",'bitcoin','ethereum','bitcoin cash','litecoin','eos','cardano','stellar','neo','iota']

rawConn = sqlite3.connect('twitterRawData.db')
rawCursor = rawConn.cursor()
rawCursor.execute("CREATE TABLE IF NOT EXISTS twitterRawData(body TEXT, recordedTime TEXT, analyzed INTEGER)")
rawCursor.close()
rawConn.commit()
rawConn.close()
class StreamListener(StreamListener):
	mentionCounter = 0
	def on_status(self, status): #function acts as a generator/iterator
		if status.retweeted:
			return
		bodyText = (str(status.text)).lower()	
		i = 0
		for i in range (0,len(coinList)):
			if ((tally(bodyText, coinList[i], coinInitialList[i]) != 0) and not("https://" in bodyText) and not("rt" in bodyText)): #checks to see if comment is relevant before writing
				rawConn = sqlite3.connect('twitterRawData.db')
				rawCursor = rawConn.cursor()
				
				currentTime = datetime.datetime.now()
				rawCursor.execute("INSERT INTO twitterRawData VALUES (?,?,0)", (bodyText,currentTime))
				rawCursor.close()
				rawConn.commit()
				rawConn.close()
				print(bodyText)
				

	def error(self, statusCode): #handles excessive request error
		if statusCode == 420:
			return False
mentionCounter = 0
stream_Listener = StreamListener()
stream = Stream(auth=api.auth, listener = stream_Listener)
stream.filter(track=trackingList)


