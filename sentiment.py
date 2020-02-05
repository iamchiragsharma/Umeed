import twitter_scraper as ts
import numpy as np
import pandas as pd
from textblob import TextBlob
import re
import pickle as pkl
import warnings
warnings.simplefilter('ignore')


def profile_hashtag_analyzer(keyword):
  "Input: Profile Name"
  "Output: List of Time,is ReTweet,Text, No of Replies, No of Retweets, No of Likes, Sentiment Polarity,OffensiveorNot"
  tweet_data = []
  for tweet in ts.get_tweets(keyword):
    tweet_data.append(tweet)

  df = pd.DataFrame(data = [tweet['time'] for tweet in tweet_data], columns=["time"])
  df['isRetweet'] = pd.DataFrame([tweet['isRetweet'] for tweet in tweet_data])
  df['text'] = np.array([tweet['text'] for tweet in tweet_data])
  df['replies'] = np.array([tweet['replies'] for tweet in tweet_data])
  df['retweets'] = np.array([tweet['retweets'] for tweet in tweet_data])
  df['likes'] = np.array([tweet['likes'] for tweet in tweet_data])
  df['sentiment_polarity'] = np.array([sentiment(tweet) for tweet in df['text']])
  df['offensive_or_not'] = np.array([hate_speech_detection(tweet) for tweet in df['text']])
  return [[df.loc[idx,"time"],df.loc[idx,"isRetweet"],df.loc[idx,"text"],
           df.loc[idx,"replies"],df.loc[idx,"retweets"],df.loc[idx,"likes"],
           df.loc[idx,"sentiment_polarity"],df.loc[idx,"offensive_or_not"]] 
          for idx in df.index]

def clean_tweet(tweet):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def sentiment(tweet):
  analysis = TextBlob(clean_tweet(tweet))
  return analysis.sentiment.polarity

def hate_speech_detection(tweet):
    loaded_model = pkl.load(open("offensive.sav", 'rb'))
    ans = loaded_model.predict([clean_tweet(tweet)])
    if ans == [1]:
        return "Offensive"
    if ans == [0]:
        return "Non-Offensive"

def get_profile(profile_name):
  "Gives you details of the profile provided"
  return ts.Profile(profile_name).to_dict()