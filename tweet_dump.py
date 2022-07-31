#!/usr/bin/env python
# encoding: utf-8

# script to download up to <= 3200 (the official API limit) of most recent tweets from a user's timeline 
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient

import tweepy
import json
import time
import configparser

# Twitter API credentials
config = configparser.ConfigParser()
config.read('config.ini')

CONSUMER_KEY = config["DEFAULT"]["CONSUMER_KEY"].strip("'\"")
CONSUMER_SECRET = config["DEFAULT"]["CONSUMER_SECRET"].strip("'\"")
ACCESS_TOKEN = config["DEFAULT"]["ACCESS_TOKEN"].strip("'\"")
ACCESS_TOKEN_SECRET = config["DEFAULT"]["ACCESS_TOKEN_SECRET"].strip("'\"")

# Hardcoded variables
OLDEST_POSTS = 2014
WINDOW = 2

class TwitterHarvester(object):
    # Create a new TwitterHarvester instance
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret,
                 wait_on_rate_limit=False):

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.secure = True
        self.auth.set_access_token(access_token, access_token_secret)
        self.__api = tweepy.API(self.auth,
                                wait_on_rate_limit=wait_on_rate_limit)
    
    @property
    def api(self):
        return self.__api

def twitter_logic(conn, company, a):
    api = a.api

    # assume there's MongoDB running on the machine, get a connection to it
    db = conn['twitter_db']
    collection = db['tweets']

    # use the cursor to skip the handling of the pagination mechanism 
    # http://docs.tweepy.org/en/latest/cursor_tutorial.html
    tweets = tweepy.Cursor(api.user_timeline, screen_name=company, tweet_mode='extended').items()

    c = 0
    tt = time.time()
    print("Starting {} processing".format(company))
    while True:
        # as long as I still have a tweet to grab
        try:
            data = tweets.next()
        except StopIteration:
            break
        # ignore old tweets
        if data.created_at.year < OLDEST_POSTS:
            break
        # convert from Python dict-like structure to JSON format
        jsoned_data = json.dumps(data._json)
        tweet = json.loads(jsoned_data)
        # insert the information in the database
        collection.insert_one(tweet)
        c += 1

        if c % 1000 == 0:
            print("Processed {} {} tweets with average {} tweets/ms".format(c, company, 1000*c / tt))

    print("Finished {} after {} seconds and {} iterations".format(company, time.time() - tt, c))


if __name__ == "__main__":
    f = open("usernames.txt", "r")

    conn = MongoClient("localhost", 27017)
    th = TwitterHarvester(CONSUMER_KEY, CONSUMER_SECRET,
                            ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                            wait_on_rate_limit=True)


    executor = ThreadPoolExecutor(max_workers = WINDOW)
    for l in f.readlines():
        executor.submit(twitter_logic, conn, l.strip(), th)

    executor.shutdown()

