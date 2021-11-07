import os
import sys
import tweepy
import string
from textblob import TextBlob
import re


CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
#print(CONSUMER_KEY,CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# create def get_tweets(query, count):
def get_tweets(query, count):
    #print("Twitter Sentiment Analysis ")

    # print(settings)
    # print(settings['access_token_secret'])
    auth = tweepy.OAuthHandler(
        CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    fetched_tweets = api.search(q=query, count=count)
    return fetched_tweets

# create def analyse(tweet):
def analyse(tweet):
    data = []
    text = tweet.text
    text = text.replace("RT", " ")
    msg = "Tweet : " + text
    data.append(msg)
    # print(dir(tweet))
    msg = "Language : " + tweet.lang
    data.append(msg)
    """Utility function to clean tweet text by removing links, special characters
    using simple regex statements.  """
    text = " ".join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    msg = "New text : " + text
    data.append(msg)
    analysis = TextBlob(text)
    # print(analysis.sentiment)
    if analysis.sentiment.polarity == 0:
        msg = "Sentiment : Neutral"
    elif analysis.sentiment.polarity > 0:
        msg = "Sentiment : Positive"
    else:
        msg = "Sentiment : Negative"
    data.append(msg)
    return data
