# Dom Smith <domlucasmith@gmail.com>

import argparse

##_______________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--counts", type=int, default=100, help="Total number of counts to fetch: max is 100")
parser.add_argument("-H", "--hashtag", default='#arsenal', help="Input hashtag")
parser.add_argument("-s", "--score",default=False, action='store_true', help="Return collection of scores")
parser.add_argument("-g", "--gossip",default=True, action='store_true', help="Return gossip from tweets")
parser.add_argument('--out-dir', default='./', help="Location of output")
parser.add_argument('--in-tweets', help="Location of tweets file")
parser.add_argument('--dry_run', action = "store_true", default = False, help = "Dry run")
parser.add_argument('--logging-level', default = 'INFO', choices = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'], help = 'level for logging')
args = parser.parse_args()
