# Multithreaded tweet dump into MongoDB

This is a short script that will download the most recent 3200 tweets from a user (the max the twitter api allows) and inserts it into a mongodb database. 

There is a ```WINDOW``` variable and an ```OLDEST_POSTS``` variable you will likely want to set. ```WINDOW``` determines how many theads will be opened by ThreadPoolExecutor to download tweets and insert them into the database. ```OLDEST_POSTS``` is a date limiter in case you want to avoid getting posts that are older than a certain year (set it to 0 to turn it off). Lastly you will have to set your own private/public key information in tweet_dump.py

## Setup

I would recommend setting a unique key index over the ```id``` twitter field, since you presumably don't want duplicate entries

You will also need a file titled usernames.txt filled with the usernames you want to search for followed by a carriage return *\n*. If you would like to add commas to the end of this, you can edit the "strip()" method how you like. I included an example file if you like.

