#!/bin/bash

sudo apt update
sudo apt install python3-pip
pip install --user pipenv
mkdir .venv
pipenv install flask
pipenv install requests

export FLASK_DEBUG=1
flask run
