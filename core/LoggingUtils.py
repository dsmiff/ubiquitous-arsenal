# Dominic Smith <dosmith@cern.ch>
'''
Module to declare logging features
'''

import os
import logging

##_______________________________________________________||
filename = 'feed_out.log'
log_dir = os.path.join(os.environ['UBIQHOME'],'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
else: pass

file_dir = os.path.join(log_dir, filename)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(filename=file_dir,level=logging.INFO)

