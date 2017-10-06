# Dominic Smith <dosmith@cern.ch>
'''
Class to alter Twitter feed i.e. convert unicode to string
'''

import os
import argparse
import time
import logging
import unicodedata
from collections import Counter
from itertools import izip_longest
from .DataUtils import DataTools
from .LoggingUtils import LogMessage

##_______________________________________________________||
class TweetTools(object):
    '''
    Args:
        counts : Total number of tweets to fetch, max is 100
        hashtag : Hashtag used to scrape tweets
        score : Flag used to return the score of a match of a given hashtag
        gossip : Flag used to return gossip of a given hashtag
        dry_run : Perform a dry run before scraping
    '''
    def __init__(self, counts, hashtag, score, gossip, out_dir, in_tweets, dry_run, logging_level):
        self.tweets = [ ]
        self.counts = counts
        self.hashtag = hashtag
        self.score = score
        self.gossip = gossip
        self.out_dir = out_dir
        self.in_tweets = in_tweets
        self.iterations = int(round(counts/100.0))
        self.params = {'q': hashtag, 'count': counts}
        self.logging_level = logging.getLevelName(logging_level)
        self.logger = logging.getLogger('Tweet tools')
        self.dataTools = DataTools()
        
    def __call__(self):
        print "Begin fetching Twitter info"
        
    def __set__(self):
        print "Altering the attributes to the tweet"
        
    def __get__(self):
        print "Getting stuff"
        
    def fetchTweets(self, twitter_handle):
        '''
        Using the twitter object, return a list of tweets from a set of parameters.
        '''
        self.logger.info("Fetching tweets with parameters {}".format(self.params))
        for i in range(0,self.iterations):
            search = twitter_handle.search(**self.params)
            tweet_list = search['statuses']
            time.sleep(2)
            self.tweets.extend(tweet_list)
            
        return self.tweets
            
    def convertText(self, text):
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        return text

    def convertToText(self,tweets):
        all_text = [self.convertText(tweet['text']) for tweet in tweets]
        self.logger.info("Writing text from tweets to file")
        if not all_text:
            print "Unable to convert text"
            sys.exit(1)
        else:
            # Store the converted tweets to a text file for later analysis
            self.dataTools.writeToFile(all_text, self.out_dir)
            return all_text

##_______________________________________________________||
class TweetFilter(TweetTools):

    cache =  {}

    def __init__(self,*args,**kwargs):
        super(TweetFilter, self).__init__(*args,**kwargs)
        self.tweets = self.dataTools.readFromFile(self.in_tweets)

    def __call__(self, hashtag, textList):
        if not textList:
            print("Received Twitter feed empty")
        else:
            if hashtag in self.__class__.cache:
                return self.__class__.cache
            branch = self.assign(hashtag, textList)
            if branch is not None:
                self.__class__.cache = branch
                return self.__class__.cache
                
            return None
            
    def assign(self, hashtag, textList):
        if self.textListEmpty(textList): return None
        if self.hashtagEmpty(hashtag): return None

        branch = {hashtag: textList}
        return branch
        
    def textListEmpty(self, textList):
        if not textList:
            return True
        else:
            return False

    def hashtagEmpty(self, hashtag):
        if not isinstance(hashtag,basestring): return True
        else: return False

    def hashtaginString(self,string,hashtag):
        if hashtag or hashtag.capital() in string: return True
        else: return False
        
    def contains_commonTitles(self, titles):
        commonTitles = ['RT', 'Arsene', 'Arsenal']
        return bool(set(commonTitles) & set(titles))
        
    def returnTopHits(self, filter_dict,hashtag):
        strings = filter_dict[hashtag]
        matches = [ ]
        for string in strings:
            if not self.hashtaginString(string, hashtag): continue
            titles = [l for l in string.split() if l[0].isupper()]
            if self.contains_commonTitles(titles): continue
            return titles

    def returnResults(self, filter_dict, hashtag):
        strings = filter_dict[hashtag]
        results = [ ]
        for string in strings:
            stringList = string.split()
            scores = [item for item in stringList if item.split('-')[0].isdigit()]
            if (scores and '-' in scores[0]):
                # Remove formations
                if scores[0].count('-') > 1: continue
                results.append(scores[0])
            else: continue

        return results
