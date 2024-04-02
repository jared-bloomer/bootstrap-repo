#!/usr/bin/env python3
#!python
# -*- coding: utf-8 -*-

"""
This script is designed to do the intial file creation in a brand new empty git repository
"""

__author__      = "Jared Bloomer"
__copyright__   = "Copyright 2024"
__credits__     = ["Jared Bloomer"]
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Jared Bloomer"
__email__       = "me@jaredbloomer.com"
__status__      = "Production"

import os
import sys
import logging
import requests
import argparse

class logs:
  def __init__ (self, file):
    loggerFormat=logging.Formatter('%(asctime)s - %(message)s')
    self.log=logging.getLogger(file)
    self.log.setLevel(logging.DEBUG)
    self.log.propagate = False # Disable Logging to stdout
    #  create file handler which logs even debug messages
    fh = logging.FileHandler(file+'.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler(stream=None)
    ch.setLevel(logging.ERROR)
    ch.propagate = False # Disable Logging to stdout
    fh.setFormatter(loggerFormat)
    ch.setFormatter(loggerFormat)
    # add the handlers to the logger
    self.log.addHandler(fh)
    self.log.addHandler(ch)

  def write_log(self, level, message, *args, **kwargs):
    if(level=="DEBUG" or level =="debug"):
      self.log.debuginfo("DEBUG - "+message, *args, **kwargs)
    elif(level=="INFO" or level =="info"):
      self.log.info("INFO - "+message, *args, **kwargs)
    elif(level=="WARN" or level =="warn"):
      self.log.warning("WARN - "+message, *args, **kwargs)
    elif(level=="ERROR" or level =="error"):
      self.log.error("ERROR - "+message, *args, **kwargs)
    elif(level=="CRITICAL" or level =="critical"):
      self.log.critical("CRIT - "+message, *args, **kwargs)
    elif(level=="EXCEPTION" or level =="exception"):
      self.log.exception(message, *args, **kwargs)



def main():
  l=logs(os.path.basename(__file__))
  l.write_log("info", "Script logger has been initialzied.")

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt as e:
    print("\n\nExiting on user cancel.", file=sys.stderr)
    sys.exit(1)
