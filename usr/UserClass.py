# Dominic Smith <dosmith@cern.ch>
'''
Class to access user credentials
'''

import os
import json

##__________________________________________||
class UserDetails(object):
    def __init__(self):
        self.content = None
        pass

    def __call__(self):
        print "Extracting detail information"
    
    @staticmethod
    def readDetails(fname):
        try:
            detail_dir = os.environ['UBIQHOME']
        except EnvironmentError:
            print("Environment variables not set")

        file_dir = os.path.join(detail_dir, fname)

        if os.path.isfile(file_dir):
            with open(file_dir,'r') as jfile:
                content = json.load(jfile)
                return content
        else:
            print("File directory not found")
            return None

    @staticmethod
    def detailsFound(details):
        if details is None:
            return False
        else:
            return True
            
