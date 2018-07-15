# Cryptoscrape
*Social media analysis program utilizing natural language processing to track cryptocurrency price trends*

This project was completed over the course of 3 months, and exposed me to several new concepts and challenges along the way. 

## Requirements and Modules Used
-PRAW

-Tweepy

-Matplotlib

## Starting off
I started this project using PRAW, a python wrapped for Reddit's streaming API. I set the api to monitor the
/r/cryptocurrency discussion board, and triggered text processing when any of the top 10 cryptocurrencies by market cap was mentioned.

Later in the project, this method was mimicked to handle data from twitter.

## Text Processing
I used a very minimalist form of natural language processing for this project, found in the Tally.py file above. The body of the comment text 
is normalized to lowercase, and parsed for a set of 'positive' and 'negative' keywords, counting each positive mention as +1 and each negative
mention as -1. These scores are summed, returned, and added to the coins net score. A weighted score is created by compensating 
for number of mentions; each coin is assigned a value between -1 and 1 based on this model.

## Handling Data Storage

Initially, I wanted to use a CSV file for data storage, due to my previous exposure with this filetype. However, I quickly realized that
this was not at all scalable. I decided to use an SQL database to store data, due to its scalability and prevalence in industry. I had to
rewrite my storage function to achieve this, but the net gain in efficiency was worth the time spent learning how to write queries and 
storage commands.

Due to the way the twitter API limits retrieval, I was forced to store the raw text from tweets in a database and analyze the data all at once. While frustrating, the data produced through this process is identical to that seen when using real-time processing.

## Data processing

Data was initially sent to output in command line, to give me a sense of what I was working with. 
![raw data](https://user-images.githubusercontent.com/40841906/42737586-ea2f3a32-8843-11e8-82ff-bfc6a729cc56.PNG)

I used Matplotlib, a pseudo-matlab python module, to visualize my data and compare it to real-world price trends.

Here, you can see my programs output of weighted score during a price reduction
![graph](https://user-images.githubusercontent.com/40841906/42737645-dbcc8da4-8844-11e8-97a3-32ab8d8f81a6.PNG)

compared to a price graph during the same time period.
![real graph](https://user-images.githubusercontent.com/40841906/42737658-f8b71682-8844-11e8-9e96-e7996f43a220.PNG)

As you can see, my NLP algorithm picked up on the price dip without retrieving any numerical values. Neat!

## Conclusion

This project was extremely satisfying to work on once it started to give me accurate results. While my goal of predicting price changes
is still underway, the fact that my algorithm can pick up on price changes without retrieving prices is deeply interesting to me, and I'm
going to continue to work on this project (and others) to explore this phenomenon.


