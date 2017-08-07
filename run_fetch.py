#!/usr/bin/env python
# Dominic Smith <dosmith@cern.ch>
'''
Fetch information off Twitter following a specific hashtag
'''

import os
import sys
import time
from core.LoggingUtils import *
from usr.UserClass import UserDetails
from core.TweetUtils import *
from core.DataUtils import *
from twython import Twython

##_______________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--counts", type=int, default=100, help="Total number of counts to fetch: max is 100")
parser.add_argument("-H", "--hashtag", default='#arsenal', help="Input hashtag")
parser.add_argument("-s", "--score",default=False, action='store_true', help="Return collection of scores")
parser.add_argument("-g", "--gossip",default=True, action='store_true', help="Return gossip from tweets")
args = parser.parse_args()

##_______________________________________________________||
def returnScore(filter_dict, hashtag):
    '''Return a collection of results 
    from a recent match
    '''
    
    filter_object = TweetFilter()
    scores = filter_object.returnResults(filter_dict, hashtag)
    return scores

##_______________________________________________________||
def returnGossip(text, hashtag):
    '''Return gossip and useful information
    from the collection of tweets obtained with
    the hashtag
    '''
    
    print "Fetching latest gossip from collection of tweets"
    keywords = ['bid','reports','according','sign']
    data_object  = DataTools(text)
    team         = hashtag.split('#')[1]
    refined_text = data_object.removeTeamPlayers(team)
    keyword_tweets = [tweet for tweet in refined_text for keyword in keywords if keyword in tweet]
    matches      = data_object.removeDuplicates(keyword_tweets)
    players = []
    for match in matches:
        hits = data_object.findTargets(match)
        for name in hits:
            last_first = HumanName(name).last + ', ' + HumanName(name).first
            players.append(last_first)
        
    print 'Players gossiped about : ', players

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

    TWITTER_APP_KEY = details['TWITTER_APP_KEY']
    TWITTER_APP_KEY_SECRET = details['TWITTER_APP_KEY_SECRET']
    TWITTER_ACCESS_TOKEN = details['TWITTER_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN_SECRET = details['TWITTER_ACCESS_TOKEN_SECRET']

    twitter = Twython(app_key=TWITTER_APP_KEY, 
                app_secret=TWITTER_APP_KEY_SECRET,
                oauth_token=TWITTER_ACCESS_TOKEN,
                oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

    tweets = []
    iterations = int(round(nCounts/100.0))
    params = {'q': hashtag, 'count':nCounts}

    for i in range(0,iterations):
        search = twitter.search(**params)
        tweet_list = search['statuses']
        time.sleep(2)
        tweets.extend(tweet_list)
        
    text = twitter_obj.convertToText(tweets)
    # Define user objects
    filter_object = TweetFilter()
    filter_dict = filter_object(hashtag, text)

    # Return data
    if scores:
        results = returnScore(filter_dict, hashtag)
    if gossip:
        gossip  = returnGossip(text, hashtag)

##_______________________________________________________||
if __name__=='__main__':
    main()
