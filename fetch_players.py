#!/usr/bin/env python
# Dom Smith <domlucasmith@gmail.com>

import os, sys, time, logging
import ConfigParser
from core.Parser import args
from core.DataUtils import UrlTools
from core.DataUtils import DataTools
import urllib2

##_______________________________________________________||
args_dict = vars(args)

ex_page = "http://www.footballsquads.co.uk/eng/2017-2018/faprem/{}.htm"

logging.basicConfig(level = logging.getLevelName(args.logging_level))
##_______________________________________________________||
def main():
    
    url_object = UrlTools(args.hashtag)
    players = url_object.getPlayersFromUrl(ex_page)
    DataTools.dumpToFile(players, players.keys()[0])
    
##_______________________________________________________||
if __name__=='__main__':
    soup = main()
