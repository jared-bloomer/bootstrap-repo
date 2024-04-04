
![GitHub License](https://img.shields.io/github/license/jared-bloomer/bootstrap-repo) ![Contributors](https://img.shields.io/github/contributors/jared-bloomer/bootstrap-repo) ![Issues](https://img.shields.io/github/issues/jared-bloomer/bootstrap-repo?color=0088ff) ![Pull Request](https://img.shields.io/github/issues-pr/jared-bloomer/bootstrap-repo?color=0088ff)

# bootstrap-repo

## Description
This python script will generate base advanced level file configuration to be placed in any newly create github repo to get your repo standards to the next level. 

## Installation

It is recommended to use a Python virtual environment to run this to ensure you are able to install the prerequisite packages in `requirements.txt` without installing them system wide. 

1. Clone down this repo with the command `git clone https://github.com/jared-bloomer/bootstrap-repo.git`
2. Change into the newly created directory with the command `cd bootstrap-repo`
3. Create a Python Virtual Environment with the command `python3 -m venv .venv`
4. Activate the new virtual environment with the command `source .venv/bin/activate`
5. Install the Python prerequisite packages with the command `pip install -r requirements.txt`
6. Run the bootstrap_repo.py script to create the files. The created files will be in an directory named `output`.

## Usage

For the full help of this script please run `./bootstrap_repo.py -h`

For most cases you can simply run `./bootstrap_repo.py -r True -o my-organization-name`
                 