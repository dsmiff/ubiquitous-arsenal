# Dominic Smith <dosmith@cern.ch>
'''
Class to perform analysis on data of tweets
'''

import os
import argparse
import unicodedata
import json
from collections import Counter

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
