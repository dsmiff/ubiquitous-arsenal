ubiquitous-arsenal
===========
Grab Twitter data related to all things Arsenal

Installation requirements
-----------

NLTK, nameparser and Twython is required.
It can be installed via pip or through a conda environment.

For Twython: ::

  pip install twython


Following which you can make a clone of this repository: ::

  git clone git@github.com:dsmiff/ubiquitous-arsenal.git
  source setup.sh

  
Running ubiquitous-arsenal: ::
  
  source setup.sh
  python fetch_tweets.py --counts <nTweets> -H <hashtag> --logging-level <logging_level>

Twython returns a maximum of 100 tweets from the search function. Therefore, nTweets is split into intervals of 100 tweets,
each interval waiting 5 seconds before moving to the next.
Logic is to filter squad players from each tweet, then search for human names using the nltk package.
Immediate weakness is the difficulty in searching only for last names.

The tweets are stored to a text file, under the directory in which the script is run.
From which, to analyse the tweets: ::

  python analyse_tweets.py --in-tweets <tweet_file>
  
