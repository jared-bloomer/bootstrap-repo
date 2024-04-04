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
__license__     = "GPL"
__version__     = "1.0.0"
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
  parser.add_argument('-r', '--readme', required=True, action='store',
    default=True,
    help='Should a README.md template be created? Value should be True or False')
  parser.add_argument('-l', '--license', required=False, action='store',
    default="MIT",
    help='Should a LICENSE file be created?')

  args = parser.parse_args(argv)
  return args

def generate_bug_template(logger):
  l=logger

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/bug.yml")
  with open("output/.github/ISSUE_TEMPLATE/bug.yml", "w") as bug:
    bug.write("""
name: 🐛Bug Report
description: File a bug report here
title: "[BUG]: "
labels: ["bug"]
assignees: ["<My Github Username>"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!!!
  - type: checkboxes
    id: new-bug
    attributes:
      label: Is there an existing issue for this?
      description: Please search to see if an issue already exists for the bug you encountered.
      options:
      - label: I have searched the existing issues
        required: true
  - type: textarea
    id: bug-description
    attributes:
      label: Description of the bug
      description: Tell us what bug you encountered and what should have happened
    validations:
      required: true
  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: Steps To Reproduce
      description: Steps to reproduce the behavior.
      placeholder: Please write the steps in a list form
    validations:
      required: true
  - type: dropdown
    id: versions
    attributes:
      label: Which version of the app are you using?
      description: If this issue is occurring on more than 1 version of the app, select the appropriate versions.
      multiple: true
      options:
       - 1.0.0
    validations:
      required: true
             """)
    bug.close()

def generate_feature_request_template(logger):
  l=logger

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/feature_request.yml")
  with open("output/.github/ISSUE_TEMPLATE/feature_request.yml", "w") as feat:
    feat.write("""
name: 🚀Feature request
description: Suggest and idea for improvement
title: "[Feat]: "
labels: ["Enhancement"]
assignees: ["<My Github Username>"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this feature request!!!
  - type: checkboxes
    id: new-feature
    attributes:
      label: Is there an existing issue/feature for this?
      description: Please search to see if an issue or feature request already exists for this.
      options:
      - label: I have searched the existing issues
        required: true
  - type: textarea
    id: feature-description
    attributes:
      label: Description of the feature
      description: Tell us what this feature is about and what it will do.
    validations:
      required: true
  - type: textarea
    id: value
    attributes:
      label: What value will this feature add?
      description: Provide examples of what value will be added by implementing the feature.
      placeholder: Please write the values in a list form
    validations:
      required: true
             """)
    feat.close()


def generate_default_files(logger, org):
  l=logger

  l.write_log("info", "Ensuring output/.github directory exist")
  if not os.path.exists("output/.github"):
    os.makedirs("output/.github")

  l.write_log("info", "Ensuring output/.github/ISSUE_TEMPLATE directory exist")
  if not os.path.exists("output/.github/ISSUE_TEMPLATE"):
    os.makedirs("output/.github/ISSUE_TEMPLATE")

  generate_bug_template(l)
  generate_feature_request_template(l)

  Path.touch("output/CHANGELOG.md") # Templated
  Path.touch("output/SUPPORT.md") # Templated
  Path.touch("output/SECURITY.md") # Templated
  Path.touch("output/CODE_OF_CONDUCT.md") # Templated
  Path.touch("output/CONTRIBUTING.md") # Templated
  Path.touch("output/CODEOWNERS.md") # Templated
  Path.touch("output/.github/ISSUE_TEMPLATE/config.yml") # Templated
  Path.touch("output/.github/PULL_REQUEST_TEMPLATE.md") # Templated

  l.write_log("info", "Creating output/CHANGELOG.md")
  with open("output/CHANGELOG.md", "w") as cl:
    cl.write("""
# Unreleased
* initial repo creation
             """)
    cl.close()

  l.write_log("info", "Creating output/.github/ISSUE_TEMPLATE/config.yml")
  with open("output/.github/ISSUE_TEMPLATE/config.yml", "w") as ic:
    ic.write("""
blank_issues_enabled: false
contact_links:
  - name: GitHub Support
    url: https://support.github.com/contact
    about: Contact Support if you're having trouble with your GitHub account.
             """)
    ic.close()

  with open("output/SECURITY.md", "w") as s:
    s.write(f"""
## Security

{org} takes the security of our software products and services seriously, which includes all source code repositories managed through our GitHub organizations.

If you believe you have found a security vulnerability in any {org}-owned repository  please report it to us as described below.

## Reporting Security Issues
            
To report a security related issue, please open an issue on this repository and describe the details using the following template

```
# Security Vulnerability Description

## Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
            
## References to any CVE's
            
## Advanced Details
### Files with security vulnerability

### Location of impacted source code (if known)

### Steps to reproduce issue
            
### Proof of concept of exploitation (if possible)
            
## Impact of Vulnerability

```
            
## Preferred Languages

We prefer all communications to be in English.
             """)
    s.close()

  with open("output/CODE_OF_CONDUCT.md", "w") as cc:
    cc.write("""
# Code of Conduct

Be nice and respectful.
             """)
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

def generate_readme(org, lic):
  with open("output/README.md", "w") as readme:
    readme.write(f"""
![Github Actions](https://github.com/{org}/<repo name>/actions/workflows/<action file name>.yml/badge.svg) ![GitHub License](https://img.shields.io/github/license/{org}/<repo name>) ![Contributors](https://img.shields.io/github/contributors/{org}/>github repo name>) ![Issues](https://img.shields.io/github/issues/{org}/<Github repo name>?color=0088ff) ![Pull Request](https://img.shields.io/github/issues-pr/{org}/<Github Repo name>?color=0088ff)

# Repo Name

## Description

## Installation

## Usage

                 """)

    readme.close()

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
  generate_default_files(l, args.organization)

  if args.readme:
    l.write_log("info", "Generating README.md file")
    generate_readme(args.organization, args.license)

  if args.license:
    l.write_log("info", "Downloading LICENSE.md file")
    get_license(l, args.license)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt as e:
    print("\n\nExiting on user cancel.", file=sys.stderr)
    sys.exit(1)
