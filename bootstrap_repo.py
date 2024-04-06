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

def generate_bug_template(logger, org):
  l=logger

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/bug.yml")
  bug_template = environment.get_template("bug.jinja2")
  bug_vars = {
    "org": org,
  }
  bug_content = bug_template.render(bug_vars)
  with open("output/.github/ISSUE_TEMPLATE/bug.yml", "w") as bug:
    bug.write(bug_content)
    bug.close()

def generate_feature_request_template(logger, org):
  l=logger

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/feature_request.yml")
  feat_template = environment.get_template("feature_requests.jinja2")
  feat_vars = {
    "org": org,
  }
  feat_content = feat_template.render(feat_vars)
  with open("output/.github/ISSUE_TEMPLATE/feature_request.yml", "w") as feat:
    feat.write(feat_content)
    feat.close()

def generate_readme(org, lic, repo):
  readme_template = environment.get_template("readme.jinja2")
  readme_vars = {
    "org": org,
    "lic": lic,
    "repo": repo,
  }
  readme_content = readme_template.render(readme_vars)
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
  changelog_template = environment.get_template("changelog.jinja2")
  changelog_vars = {}
  changelog_content = changelog_template.render(changelog_vars)
  with open("output/CHANGELOG.md", "w") as cl:
    cl.write(changelog_content)
    cl.close()

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/config.yml")
  ic_template = environment.get_template("issue_config.jinja2")
  ic_vars = {}
  ic_content = ic_template.render(ic_vars)
  with open("output/.github/ISSUE_TEMPLATE/config.yml", "w") as ic:
    ic.write(ic_content)
    ic.close()

  security_template = environment.get_template("security.jinja2")
  security_vars = {
    "org": org,
  }
  security_content = security_template.render(security_vars)
  with open("output/SECURITY.md", "w") as s:
    s.write(security_content)
    s.close()

  coc_template = environment.get_template("code_of_conduct.jinja2")
  coc_vars = {}
  coc_content = coc_template.render(coc_vars)
  with open("output/CODE_OF_CONDUCT.md", "w") as cc:
    cc.write(coc_content)
    cc.close()

  with open("output/CONTRIBUTING.md", "w") as c:
    c.write("""
## Development

### Fork, Clone, Branch, and Create your Pull Request

To Contribute to this repositiry please following the steps below. 

1. Fork the repository if you have not already
2. Clone your fork down locally to your machine
3. Create and push a feature branch
4. Make your changes and push them to your feature branch
5. Open a pull request and include details of your change and any testing you have done in the pull request description. If possible please use [Conventional Commits](https://www.conventionalcommits.org/)
            
### Code Review

We require all Pull Request to be revviewed by Code Owners in this repository. No Pull Request will be merged in to this repository without a code review. 

Once your code has been reviewed and approved by the requisite number of team members, it will be merged into the main branch. Once merged, your PR will be automatically closed.
            """)        
    c.close()

  with open("output/SUPPORT.md", "w") as support:
    support.write("""
# Support

## How to file issues and get help  

This project uses [GitHub issues][gh-issue] to [track bugs][gh-bug] and [feature requests][gh-feature]. Please search the existing issues before filing new issues to avoid duplicates. For new topics, file your bug or feature request as a new issue.
""")
    support.close()

  with open("output/.github/PULL_REQUEST_TEMPLATE.md", "w") as prt:
    prt.write("""
## Summary of the Pull Request

## References and Relevant Issues

## Detailed Description of the Pull Request / Additional comments

## Validation Steps Performed

## PR Checklist
- [ ] Closes #xxx
- [ ] Tests added/passed
- [ ] Documentation updated
   - If checked, please file a pull request and link it here: #xxx
- [ ] Schema updated (if necessary)
             """)
    prt.close()

  with open("output/CODEOWNERS.md", "w") as co:
    co.write(f"""
# Code owners file.
# This file controls who is tagged for review for any given pull request.
* @{org}

# For anything not explicitly taken by someone else:
* @{org}/team-name
            """)
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

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt as e:
    print("\n\nExiting on user cancel.", file=sys.stderr)
    sys.exit(1)
