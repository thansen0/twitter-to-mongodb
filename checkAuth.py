#!/usr/bin/env python
# encoding: utf-8

# Ensures the API keys are correct
import tweepy
import configparser

# Twitter API credentials
config = configparser.ConfigParser()
config.read('config.ini')

CONSUMER_KEY = config["DEFAULT"]["CONSUMER_KEY"].strip("'\"")
CONSUMER_SECRET = config["DEFAULT"]["CONSUMER_SECRET"].strip("'\"")
ACCESS_TOKEN = config["DEFAULT"]["ACCESS_TOKEN"].strip("'\"")
ACCESS_TOKEN_SECRET = config["DEFAULT"]["ACCESS_TOKEN_SECRET"].strip("'\"")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

id = 1549380685856751616

status = api.get_status(id, tweet_mode="extended")

# We use text in normal mode
# print(status.text)

# And full_text in extended mode
print(status.full_text)
