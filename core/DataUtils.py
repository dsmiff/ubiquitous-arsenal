# Dominic Smith <dosmith@cern.ch>
'''
Class to perform analysis on data of tweets
'''

import os
import argparse
import unicodedata
import json
import nltk
import time
import logging
from collections import Counter, defaultdict
from nameparser.parser import HumanName

##_______________________________________________________||
class DataTools(object):
    def __init__(self):
        self.outputDir = os.path.dirname(os.path.realpath(__file__))
        self.logger = logging.getLogger('Data tools')
        
    def __call__(self):
        print "Performing data analysis on tweets"

    def removeTeamPlayers(self, team):
        '''Filters the tweets by removing players of team provided
        by the hashtag
        '''
        print "Removing team players from squad: ", team
        
        squad = self.loadSquad(team)
        numbers = squad.keys()
        players = squad.values()

        self.tweets = [tweet for tweet in self.tweets if not any(player in tweet for player in players)]

        return self.tweets
    
    def findNames(self):

        pass

    def loadSquad(self, team):
        '''Load the list of players from a team
        '''
        squads = os.path.join(os.environ['UBIQHOME'], 'squads.json')
        if os.path.isfile(squads):
            with open(squads, 'r') as jsquad:
              squad = json.load(jsquad)
              if isinstance(squad, dict):
                  return squad[team.capitalize()]
              else: print "Squad not extracted with team: ", team
        else:
            print "Unable to load team squad"
            return None
        
    def removeDuplicates(self, text):
        '''Remove duplicate tweets
        '''
        return list(set(text))
        
    def findTargets(self, text):
        '''Find human names in text
        Taken from: https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk
        '''
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary = False)
        player_list = []
        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: #avoid grabbing lone surnames
                for part in person:
                    name += part + ' '
                if name[:-1] not in player_list:
                    player_list.append(name[:-1])
                name = ''
            person = []
        return player_list

    def findDuplicates(self, players):
        tally = defaultdict(list)
        for i, player in enumerate(players):
            tally[player].append(i)
        return tally
    
    def findGossip(self, tweets, keywords, hashtag):
        self.tweets = tweets
        self.hits = {}
        self.logger.info("Fetching latest gossip from collection of tweets")
        keywords =[ ] # ['bid','reports','according','sign']
        team         = hashtag.split('#')[1]
        refined_text = self.tweets #self.removeTeamPlayers(team)
        keyword_tweets = refined_text #[tweet for tweet in refined_text for keyword in keywords if keyword in tweet]
        tweets      = self.removeDuplicates(keyword_tweets)
        players = []
        for match in tweets:
            hits = self.findTargets(match)
            for name in hits:
                last_first = HumanName(name).last + ', ' + HumanName(name).first
                players.append(last_first)

        players = self.findDuplicates(players)
        self.hits = {player: len(hit) for player, hit in players.iteritems()}
        self.logger.info('Things gossiped about {}'.format(self.hits))

    def writeToFile(self, text_list, out_dir):
        '''
        Write the text conversion to a file for later use. Will assume output directory
        is current directory.
        '''
        time_str = time.strftime("%Y%m%d-%H%M%S")
        with open(os.path.join(out_dir, 'tweets_{}.txt'.format(time_str)),"a") as f:            
            for item in text_list:
                if not self.filterText(item): continue
                f.write("%s\n" % item)
            f.close()

    def filterText(self, text):
        '''
        Need to remove new lines otherwise they are treated as another tweet.
        '''
        if '\n' in text: return False
        return True
            
    @staticmethod
    def readFromFile(input_dir):
        '''
        Read in tweets from input file. At this point, there should be no new lines '\n' in each tweet.
        '''
        print "Reading tweets from input file: {}".format(input_dir)
        if os.path.isfile(input_dir):
            with open(input_dir, "r") as f:
                content = f.readlines()
            content = [x.strip() for x in content]

        else:
            self.logger.error("Unable to find input text file")
        return content        
