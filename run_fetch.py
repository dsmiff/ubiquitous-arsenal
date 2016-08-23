# Dominic Smith <dosmith@cern.ch>
'''
Fetch information off Twitter following a specific hashtag
'''

import os
import sys
import logging
from usr.UserClass import UserDetails
from core.TweetUtils import TweetTools
from twython import Twython

##_______________________________________________________||
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(filename='twitter_out.log',level=logging.INFO)

##_______________________________________________________||
def main():
    
    my_details = UserDetails()
    twitter_obj = TweetTools()
    
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
    
    search = t.search(q='#arsenal',   
                      count=100)

    tweets = search['statuses']
    text = twitter_obj.convertToText(tweets)
    print text

    for tweet in tweets:
        print tweet['id_str'], '\n', tweet['text'], '\n\n\n'

##_______________________________________________________||
if __name__=='__main__':
    main()
