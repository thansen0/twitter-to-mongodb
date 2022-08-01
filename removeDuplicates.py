#!/usr/bin/env python
# encoding: utf-8

# script to download up to <= 3200 (the official API limit) of most recent tweets from a user's timeline 
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient

import tweepy
import json
import time
import configparser

if __name__ == "__main__":
    conn = MongoClient("localhost", 27017)

    db = conn['twitter_db']
    collection = db['tweets']

    for tweet in db.tweets.find():
        tweet_id = tweet['id']
        num_tweets = len(list(db.tweets.find({"id":tweet_id})))
        if num_tweets > 1:
            # remove tweet
            print("Duplicate with ID: " + str(tweet_id))

            collection.delete_one({'id':tweet_id})


