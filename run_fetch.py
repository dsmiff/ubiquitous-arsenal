#!/usr/bin/env python
# Dominic Smith <dosmith@cern.ch>
'''
Fetch information off Twitter following a specific hashtag
'''

import os
import sys
import time
import ConfigParser
from core.LoggingUtils import *
from usr.UserClass import UserDetails
from core.TweetUtils import *
from core.DataUtils import DataTools
from twython import Twython

##_______________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--counts", type=int, default=100, help="Total number of counts to fetch: max is 100")
parser.add_argument("-H", "--hashtag", default='#arsenal', help="Input hashtag")
parser.add_argument("-s", "--score",default=False, action='store_true', help="Return collection of scores")
parser.add_argument("-g", "--gossip",default=True, action='store_true', help="Return gossip from tweets")
args = parser.parse_args()

##_______________________________________________________||
config = ConfigParser.ConfigParser()
config.read('my_details.cfg')

TWITTER_APP_KEY = config.get('credentials','app_key')
TWITTER_APP_KEY_SECRET = config.get('credentials','app_secret')
TWITTER_ACCESS_TOKEN = config.get('credentials','oath_token')
TWITTER_ACCESS_TOKEN_SECRET = config.get('credentials','oath_token_secret')

##_______________________________________________________||
def main():

    logger.info(LogMessage('-------------------'))
    
    my_details = UserDetails()
    twitter_obj = TweetTools()
    nCounts = int(args.counts)
    hashtag = args.hashtag
    scores  = args.score
    gossip  = args.gossip

    logger.info(LogMessage('nTweets: {nTweets}', nTweets=nCounts))
    logger.info(LogMessage('Hashtag: {hashtag}', hashtag=hashtag))
    
    details = my_details.readDetails('my_details.json')
    if not my_details.detailsFound(details):
        log.error("Cannot find any user details")
        sys.exit(1)

    twitter = Twython(app_key=TWITTER_APP_KEY, 
                app_secret=TWITTER_APP_KEY_SECRET,
                oauth_token=TWITTER_ACCESS_TOKEN,
                oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    twitter.verify_credentials()
    
    tweets = []
    iterations = int(round(nCounts/100.0))
    params = {'q': hashtag, 'count':nCounts}

    tweets = twitter_obj.fetchTweets(iterations, twitter, params)    
    text = twitter_obj.convertToText(tweets)
    # Define user objects
    filter_object = TweetFilter()
    filter_dict = filter_object(hashtag, text)

    # Return data
    if gossip:
        keywords = ['bid','reports','according','sign']
        gossip  = DataTools(text).findGossip(text, keywords, hashtag)

##_______________________________________________________||
if __name__=='__main__':
    main()
