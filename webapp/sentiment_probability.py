import os
import tweepy
import re
import urllib.request
import urllib.parse
import json

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
#print(CONSUMER_KEY,CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


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
    parameters = urllib.parse.urlencode({"text": text})
    req = urllib.request.urlopen(
        "http://text-processing.com/api/sentiment/", parameters.encode())
    result = req.read().decode()
    # print(result)
    result = json.loads(result)
    data.append(result)
    data.append("Sentiment: " + result['label'])
    # print(sentiment)
    # print(data)
    return data


def analyse_string(string):
    data = []
    msg = "Text: " + string
    data.append(msg)
    parameters = urllib.parse.urlencode({"text": string})
    req = urllib.request.urlopen(
        "http://text-processing.com/api/sentiment/", parameters.encode())
    result = req.read().decode()
    # print(result)
    result = json.loads(result)
    data.append(result)
    data.append("Sentiment: " + result['label'])
    # print(sentiment)
    # print(data)
    return data


if __name__ == '__main__':
    tweets = get_tweets(query="India", count=1)
    for tweet in tweets:
        analyse(tweet)
