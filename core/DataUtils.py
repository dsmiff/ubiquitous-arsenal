# Dominic Smith <dosmith@cern.ch>
'''
Class to perform analysis on data of tweets
'''

import os
import argparse
import unicodedata
import json
import nltk
from collections import Counter
from nameparser.parser import HumanName

##_______________________________________________________||
class DataTools(object):
    def __init__(self, tweets):
        self.tweets = tweets

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

    def findGossip(self, filter_dict, keywords, hashtag):
        print "Fetching latest gossip from collection of tweets"
        keywords = ['bid','reports','according','sign']
        team         = hashtag.split('#')[1]
        refined_text = self.removeTeamPlayers(team)
        keyword_tweets = [tweet for tweet in refined_text for keyword in keywords if keyword in tweet]
        matches      = self.removeDuplicates(keyword_tweets)
        players = []
        for match in matches:
            hits = self.findTargets(match)
            for name in hits:
                last_first = HumanName(name).last + ', ' + HumanName(name).first
                players.append(last_first)
                
        print 'Players gossiped about : ', players
