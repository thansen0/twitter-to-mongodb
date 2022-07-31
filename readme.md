# Multithreaded tweet dump into MongoDB

This is a short script that will download the most recent 3200 tweets from a user (the max the twitter api allows) and inserts it into a mongodb database using the [cursor API](https://docs.tweepy.org/en/latest/v1_pagination.html#tweepy.Cursor). 

## Setup

There is a ```WINDOW``` variable and an ```OLDEST_POSTS``` variable you will likely want to set. ```WINDOW``` determines how many theads will be opened by ThreadPoolExecutor to download tweets and insert them into the database. ```OLDEST_POSTS``` is a date limiter in case you want to avoid getting posts that are older than a certain year (set it to 0 to turn it off). Lastly you will have to set your own private/public key information in tweet_dump.py

You will additionally have to start your mongodb instance. The default names are "twitter_db" for the database and "tweets" for the collection. In some linux builds you may have to start the mongod systemctl service from the command line as well

I would also recommend setting a unique key index over the ```id``` twitter field, since you presumably don't want duplicate entries

Finally you will need a file titled usernames.txt filled with the usernames you want to search for followed by a carriage return *\n*. If you would like to add commas to the end of this, you can edit the "strip()" method how you like. I included an example username.txt file.

## Running Program

In the command line, run

```
$ python3 tweet_dump.py
```

And this should populate the database with the most recent 3200 tweets from whatever date you specified for each username in username.txt

As a helpful reminder you may run 

```
git update-index --assume-unchanged config.ini
git update-index --assume-unchanged usernames.txt
```

So that you won't accidentally push your secret tokens and username list.
