#!/usr/bin/env bash

# Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/TeamBasedLearning/Service'

PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
apt-get update
apt-get install -y python3-dev sqlite python-pip supervisor nginx git

# Upgrade pip to the latest version.
pip install --upgrade pip
pip install virtualenv

# Create a path and clone the project git on it
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/Service

# Create a virtual env path
mkdir -p $VIRTUALENV_BASE_PATH
virtualenv  $VIRTUALENV_BASE_PATH/tbl

# execute the virtualenv and install dependencies
source $VIRTUALENV_BASE_PATH/tbl/bin/activate
pip install -r $PROJECT_BASE_PATH/Service/tbl/requirements.txt

# Go to project path
cd $PROJECT_BASE_PATH/Service/tbl

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/Service/deploy/supervisor_tbl.conf /etc/supervisor/conf.d/tbl.conf
supervisorctl reread
supervisorctl update
supervisorctl restart tbl

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/Service/deploy/nginx_tbl.conf /etc/nginx/sites-available/tbl.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/tbl.conf /etc/nginx/sites-enabled/tbl.conf
systemctl restart nginx.service

echo "DONE!!!"
