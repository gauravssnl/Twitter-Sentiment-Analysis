import tweepy
from textblob import TextBlob
import re

settings = {}
config = "config.ini"
with open(config) as f:
    for line in f:
        line = line.strip()
        data = (line.split("="))
        settings[data[0].strip()] = eval(data[1])


def get_tweets(query, count):
    #print("Twitter Sentiment Analysis ")

    # print(settings)
    # print(settings['access_token_secret'])
    auth = tweepy.OAuthHandler(
        settings['consumer_key'], settings['consumer_secret'])
    auth.set_access_token(settings['access_token'],
                          settings['access_token_secret'])
    api = tweepy.API(auth)

    fetched_tweets = api.search(q=query, count=count)
    return fetched_tweets


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
