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
this was not at all scalable. I decided to use an SQL database to store data, due to its scalability and prevelance in industry. I had to
rewrite my storage function to achieve this, but the net gain in efficiency was worth the time spent learning how to write queries and 
storage commands.

## Data processing

Data was initially sent to output in command line, to give me a sense of what I was working with. 
![image](/images/raw data.PNG)
