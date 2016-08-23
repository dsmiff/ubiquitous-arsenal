import os
import unicodedata

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
