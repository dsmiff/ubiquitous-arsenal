import unittest
import json
import os

hashtag = '#Arsenal'

##_____________________________________________________________________||
class TestSquad(unittest.TestCase):

    def test_loadJson(self):

        main_env = os.environ['UBIQHOME']
        squad_name = 'squads.json'
        squad_path = os.path.join(main_env, squad_name)
        if os.path.isfile(squad_path):
            with open(squad_path, 'r') as jfile:
                squads = json.load(jfile)
                self.assertTrue(isinstance(squads, dict))

    def test_team(self):
        team = hashtag.split('#')[1]
        self.assertTrue(team=='Arsenal')

    def test_loadSquad(self):

        main_env = os.environ['UBIQHOME']
        squad_name = 'squads.json'
        squad_path = os.path.join(main_env, squad_name)
        if os.path.isfile(squad_path):
            with open(squad_path, 'r') as jfile:
                squads = json.load(jfile)

##_____________________________________________________________________||
if __name__ == '__main__':
    unittest.main()
