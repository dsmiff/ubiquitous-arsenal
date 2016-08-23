import os
import json

##__________________________________________||
class UserDetails(object):
    def __init__(self):
        pass

    @staticmethod
    def readDetails(fname):
        try:
            detail_dir = os.environ['UBIQHOME']
        except EnvironmentError:
            print("Environment variables not set")

        file_dir = os.path.join(detail_dir, fname)

        if os.path.isfile(file_dir):
            with open(file_dir) as jfile:
                content = json.load(jfile)
                return content
        else:
            return None
