#!/usr/bin/env python
# Dom Smith <domlucasmith@gmail.com>

import os, sys, time, logging
import ConfigParser
from usr.UserClass import UserDetails
from core.TweetUtils import TweetFilter
from core.DataUtils import DataTools
from core.Parser import args
from twython import Twython

##_______________________________________________________||
args_dict = vars(args)

logging.basicConfig(level = logging.getLevelName(args.logging_level))
##_______________________________________________________||
def main():

    filter_object = TweetFilter(**args_dict)

    keywords = ['bid','reports','according','sign']
    gossip  = DataTools().findGossip(filter_object.tweets, keywords, filter_object.hashtag)

##_______________________________________________________||
if __name__=='__main__':
    main()

    
    
