def tally(commentText, coin, coinInitial):
	negCount = 0
	posCount = 0
	
	negKeywords = ['sell','dump','crash','plummet','fraud','scam','shitcoin',
	'bitcoin clone','collapse','bad buy','no growth','fud']
	
	#to balance for the negative attitude of the internet, there are more positive triggers... weightedScore normalized between .2 and .4, roughly
	
	posKeywords = ['buy','surge','pump','exciting','new tech','big moves','upward','good buy',
	'growth','positive','great','moon','big things','great buy','amazing','hype train',
	'price double','new market','increased demand','whales buying','good feeling']
	
	
	if ((coin in commentText) or (coinInitial in commentText)): # send COIN, coin initials to function in function call
		for keyword in negKeywords:
			if (keyword in commentText):
				negCount = negCount + 1	
		for keyword in posKeywords:
			if (keyword in commentText):
				posCount = posCount + 1
	netCount = posCount - negCount
	return netCount