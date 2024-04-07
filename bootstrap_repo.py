#!/usr/bin/env python3
#!python
# -*- coding: utf-8 -*-

from __future__ import annotations

"""
This script is designed to do the intial file creation in a brand new empty git repository
"""

__author__      = "Jared Bloomer"
__copyright__   = "Copyright 2024"
__credits__     = ["Jared Bloomer"]
__license__     = "GPL-3.0"
__version__     = "1.1.0"
__maintainer__  = "Jared Bloomer"
__email__       = "me@jaredbloomer.com"
__status__      = "Production"

from collections.abc import Sequence
import os
import sys
from pathlib import Path
import logging
import requests
import argparse
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/"), autoescape=True)

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

def get_args(argv: Sequence[str] | None = None) -> int:
  parser=argparse.ArgumentParser(description="Bootstrap a New Github Repository",
    prog="bootstrap_repo.py",
    epilog="Developed and Maintained by Jared Bloomer me@jaredbloomer.com")
  parser.add_argument('-o', '--organization', required=True, action='store',
    default=True,
    help='Name of Github user or organization this repo is under.')
  parser.add_argument('-r', '--repo', required=True, action='store',
    default=True,
    help='Name of Github Repo')
  parser.add_argument('-l', '--license', required=False, action='store',
    default="MIT",
    help='Should a LICENSE file be created?')

  args = parser.parse_args(argv)
  return args

def get_file_contents(file, context):
    template = environment.get_template(file)
    content = template.render(context)
    return content

def generate_bug_template(logger, org):
  l=logger

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/bug.yml")
  bug_vars = {
    "org": org,
  }
  bug_content = get_file_contents("bug.jinja2", bug_vars)
  with open("output/.github/ISSUE_TEMPLATE/bug.yml", "w") as bug:
    bug.write(bug_content)
    bug.close()

def generate_feature_request_template(logger, org):
  l=logger

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/feature_request.yml")
  feat_vars = {
    "org": org,
  }
  feat_content = get_file_contents("feature_requests.jinja2", feat_vars)
  with open("output/.github/ISSUE_TEMPLATE/feature_request.yml", "w") as feat:
    feat.write(feat_content)
    feat.close()

def generate_readme(org, lic, repo):
  readme_vars = {
    "org": org,
    "lic": lic,
    "repo": repo,
  }
  readme_content = get_file_contents("readme.jinja2", readme_vars)
  with open("output/README.md", "w") as readme:
    readme.write(readme_content)
    readme.close()

def generate_default_files(logger, org, lic, repo):
  l=logger

  l.write_log("info", "Ensuring output/.github directory exist")
  if not os.path.exists("output/.github"):
    os.makedirs("output/.github")

  l.write_log("info", "Ensuring output/.github/ISSUE_TEMPLATE directory exist")
  if not os.path.exists("output/.github/ISSUE_TEMPLATE"):
    os.makedirs("output/.github/ISSUE_TEMPLATE")

  generate_bug_template(l, org)
  generate_feature_request_template(l, org)
  l.write_log("info", "Generating README.md file")
  generate_readme(org, lic, repo)

  l.write_log("info", "Creating output/CHANGELOG.md")
  changelog_vars = {}
  changelog_content = get_file_contents("changelog.jinja2", changelog_vars)
  with open("output/CHANGELOG.md", "w") as cl:
    cl.write(changelog_content)
    cl.close()

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/config.yml")
  ic_vars = {}
  ic_content = get_file_contents("issue_config.jinja2", ic_vars)
  with open("output/.github/ISSUE_TEMPLATE/config.yml", "w") as ic:
    ic.write(ic_content)
    ic.close()

  l.write_log("info", "Creating output/SECURITY.md")
  security_vars = {
    "org": org,
  }
  security_content = get_file_contents("security.jinja2", security_vars)
  with open("output/SECURITY.md", "w") as s:
    s.write(security_content)
    s.close()

  l.write_log("info", "Creating output/CODE_OF_CONDUCT.md")
  coc_vars = {}
  coc_content = get_file_contents("code_of_conduct.jinja2", coc_vars)
  with open("output/CODE_OF_CONDUCT.md", "w") as cc:
    cc.write(coc_content)
    cc.close()

  l.write_log("info", "Creating output/CONTRIBUTING.md")
  contrib_vars = {}
  contrib_content = get_file_contents("contributing.jinja2", contrib_vars)
  with open("output/CONTRIBUTING.md", "w") as c:
    c.write(contrib_content)        
    c.close()

  l.write_log("info", "Creating output/SUPPORT.md")
  support_vars = {}
  support_content = get_file_contents("support.jinja2", support_vars)
  with open("output/SUPPORT.md", "w") as support:
    support.write(support_content)
    support.close()

  l.write_log("info", "Creating output/.github/PULL_REQUEST_TEMPLATE.md")
  pr_vars = {}
  pr_content = get_file_contents("pull_request_template.jinja2", pr_vars)
  with open("output/.github/PULL_REQUEST_TEMPLATE.md", "w") as prt:
    prt.write(pr_content)
    prt.close()

  l.write_log("info", "Creating output/CODEOWNERS.md")
  co_vars = {
    "org": org,
  }
  co_content = get_file_contents("codeowners.jinja2", co_vars)
  with open("output/CODEOWNERS.md", "w") as co:
    co.write(co_content)
    co.close()

def get_license(logger, license):
  l=logger
  lic=license

  l.write_log("info", f"Attempting to locate {lic} License file. All valid Licenses support can be found at https://github.com/OpenSourceOrg/licenses/tree/master/texts/plain")
  base_url="https://github.com/OpenSourceOrg/licenses/raw/master/texts/plain/"
  response=requests.get(base_url+lic)
  if response.status_code == 200:
    l.write_log("info", f"Downloading {lic} License file.")
    with open("output/LICENSE.md", "w") as licfile:
      licfile.write(response.text)
    licfile.close()
  else:
    l.write_log("Error", f"Could not download {lic} license file. All valid Licenses support can be found at https://github.com/OpenSourceOrg/licenses/tree/master/texts/plain")

def main():
  l=logs(os.path.basename(__file__))
  try:
    l.write_log("info", "Script logger has been initialzied.")
    args = get_args()

    l.write_log("info", "Ensuring output directory exist")
    if not os.path.exists("output"):
      os.makedirs("output")

    l.write_log("info", "Generating Default Files")
    generate_default_files(l, args.organization, args.license, args.repo)

    if args.license:
      l.write_log("info", "Downloading LICENSE.md file")
      get_license(l, args.license)
  except Exception as e:
    l.write_log("error", e)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt as e:
    print("\n\nExiting on user cancel.", file=sys.stderr)
    sys.exit(1)
