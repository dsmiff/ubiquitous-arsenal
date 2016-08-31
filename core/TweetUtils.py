# Dominic Smith <dosmith@cern.ch>
'''
Class to alter Twitter feed i.e. convert unicode to string
'''

import os
import argparse
import unicodedata
from collections import Counter
from itertools import izip_longest

##_______________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--counts", default=100, help="Total number of counts to fetch")
parser.add_argument("-H", "--hashtag", default='#arsenal', help="Input hashtag")
args = parser.parse_args()

##_______________________________________________________||
class TweetTools(object):
    def __init__(self):
        pass

    def convertText(self,text):
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        return text

    def convertToText(self,tweets):
        all_text = [self.convertText(tweet['text']) for tweet in tweets]
        return all_text

##_______________________________________________________||
class TweetFilter(object):
    
    cache =  {}
    
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
        if not type(hashtag) is str: return True
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
