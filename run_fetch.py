#!/usr/bin/env python
# Dominic Smith <dosmith@cern.ch>
'''
Fetch information off Twitter following a specific hashtag
'''

import os
import sys
from core.LoggingUtils import *
from usr.UserClass import UserDetails
from core.TweetUtils import *
from twython import Twython

##_______________________________________________________||
def main():
    
    my_details = UserDetails()
    twitter_obj = TweetTools()
    nCounts = args.counts
    hashtag = args.hashtag
    
    details = my_details.readDetails('my_details.json')
    if not my_details.detailsFound(details):
        log.error("Cannot find any user details")
        sys.exit(1)
    
    TWITTER_APP_KEY = details['TWITTER_APP_KEY']
    TWITTER_APP_KEY_SECRET = details['TWITTER_APP_KEY_SECRET']
    TWITTER_ACCESS_TOKEN = details['TWITTER_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN_SECRET = details['TWITTER_ACCESS_TOKEN_SECRET']

    t = Twython(app_key=TWITTER_APP_KEY, 
                app_secret=TWITTER_APP_KEY_SECRET,
                oauth_token=TWITTER_ACCESS_TOKEN,
                oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    
    search = t.search(q=hashtag,   
                      count=nCounts)

    tweets = search['statuses']
    text = twitter_obj.convertToText(tweets)

    filter_text = TweetFilter()
    filter_dict = filter_text(hashtag,text)

    results = filter_text.returnResults(filter_dict,hashtag)
    #    for tweet in tweets:
#        print tweet
        #        print tweet['id_str'], '\n', tweet['text'], '\n\n\n'

##_______________________________________________________||
if __name__=='__main__':
    main()
