import tweepy
from textblob import TextBlob
import  re

print("Twitter Sentiment Analysis ")
settings = {}
config = "config.ini"
with open(config) as f:
	for line in f:
		line = line.strip()
		data=(line.split("="))
		settings[data[0].strip()] = eval(data[1])
#print(settings)
#print(settings['access_token_secret'])
auth = tweepy.OAuthHandler(settings['consumer_key'], settings['consumer_secret'])
auth.set_access_token(settings['access_token'], settings['access_token_secret'])
api=tweepy.API(auth)
query = input("Enter hastag to search:")
print("_"*40)
count = 20
fetched_tweets = api.search(q=query, count=count)
for tweet in fetched_tweets:
	text = tweet.text
	print(text)
	"""Utility function to clean tweet text by removing links, special characters
        using simple regex statements.  """
	text = " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
	print("New text: "+ text)
	analysis = TextBlob(text)
	print(analysis.sentiment)
	if analysis.sentiment.polarity == 0:
		print("Sentiment: Neutral")
	elif analysis.sentiment.polarity > 0:
		print("Sentiment: Positive")
	else:
		print("Sentiment: Negative")
	print("_"*40)
