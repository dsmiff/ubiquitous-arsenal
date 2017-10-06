# Dominic Smith <dosmith@cern.ch>
'''
Module to declare logging features
'''

import os
import logging

##_______________________________________________________||
class LogMessage(object):
    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)
    
