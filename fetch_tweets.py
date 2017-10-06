#!/usr/bin/env python
# Dom Smith <domlucasmith@gmail.com>

import os, sys, time, logging
import ConfigParser
from usr.UserClass import UserDetails
from core.TweetUtils import TweetTools
from core.Parser import args
from twython import Twython

##_______________________________________________________||
args_dict = vars(args)
config = ConfigParser.ConfigParser()
config.read('my_details.cfg')

TWITTER_APP_KEY = config.get('credentials','app_key')
TWITTER_APP_KEY_SECRET = config.get('credentials','app_secret')
TWITTER_ACCESS_TOKEN = config.get('credentials','oath_token')
TWITTER_ACCESS_TOKEN_SECRET = config.get('credentials','oath_token_secret')

logging.basicConfig(level = logging.getLevelName(args.logging_level))
##_______________________________________________________||
def main():
    
    my_details = UserDetails()
    details = my_details.readDetails('my_details.json')
    twitter_obj = TweetTools(**args_dict)

    twitter = Twython(app_key=TWITTER_APP_KEY, 
                      app_secret=TWITTER_APP_KEY_SECRET,
                      oauth_token=TWITTER_ACCESS_TOKEN,
                      oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    twitter.verify_credentials()

    tweets = twitter_obj.fetchTweets(twitter)
    text   = twitter_obj.convertToText(tweets)

##_______________________________________________________||
if __name__=='__main__':
    main()
