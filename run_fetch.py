import os, sys
from usr.UserClass import UserDetails
from twython import Twython

##_______________________________________________________||
def main():
    
    my_details = UserDetails()
    details = my_details.readDetails('my_details.json')

    TWITTER_APP_KEY = details['TWITTER_APP_KEY']
    TWITTER_APP_KEY_SECRET = details['TWITTER_APP_KEY_SECRET']
    TWITTER_ACCESS_TOKEN = details['TWITTER_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN_SECRET = details['TWITTER_ACCESS_TOKEN_SECRET']

    t = Twython(app_key=TWITTER_APP_KEY, 
                app_secret=TWITTER_APP_KEY_SECRET,
                oauth_token=TWITTER_ACCESS_TOKEN,
                oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    
    search = t.search(q='#arsenal',   
                      count=100)

    tweets = search['statuses']

    for tweet in tweets:
        print tweet['id_str'], '\n', tweet['text'], '\n\n\n'

##_______________________________________________________||
if __name__=='__main__':
    main()
