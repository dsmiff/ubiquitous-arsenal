import os

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
            with open(file_dir) as f:
                content = f.readlines()
                print content
                print type(content)
                print len(content)
                return content
        else:
            return None
