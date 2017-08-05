ubiquitous-arsenal
===========
Grab Twitter data related to all things Arsenal

Installation requirements
-----------

Twython is required.
It can be installed via pip.

For Twython: ::

  pip install twython


Following which you can make a clone of this repository: ::

  git clone git@github.com:dsmiff/ubiquitous-arsenal.git
  source setup.sh

  
Running ubiquitous-arsenal: ::
  source setup.sh
  python run_fetch.py -n <nTweets> -H <hashtag>

Twython returns a maximum of 100 tweets from the search function. Therefore, nTweets is split into intervals of 100 tweets,
each interval waiting 5 seconds before moving to the next.

