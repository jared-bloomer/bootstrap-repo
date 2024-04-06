# Unreleased
* Moved Readme creation to default files Generates
* Changed `-r` argument to repo name
* Added repo name to README.md templating
* Added jinja2 package to requirements.txt
* Implement jinja2 templating for
    * .github/ISSUE_TEMPLATE/bug.yml
    * .github/ISSUE_TEMPLATE/feature_request.yml
    * .github/ISSUE_TEMPLATE/config.yml
    * README.md
    * CHANGELOG.md
    * CODE_OF_CONDUCT.md
    * SECURITY.md
    * CONTRIBUTING.md
    * SUPPORT.md
    * .github/PULL_REQUEST_TEMPLATE.md
    * CODEOWNERS.md
* Wrapped main logic in try/except statement to write Exceptions to log file

# v1.1.0
* Added `-l`, `--license` option to generate a `LICENSE.md` file in the root of the repo
* Updated `README.md` to use Badging for whatever license the Repo is configured to use.

# v1.0.01
* Updated Help message for `-r`, `--readme` option in bootstrap_repo.py

# v1.0.0
* initial repo creation
             