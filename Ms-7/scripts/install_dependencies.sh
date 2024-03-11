#!/bin/bash
# kill any servers that may be running in the background 
sudo pkill -f runserver
sudo pkill -f 'celery -A news_app worker --loglevel=info'
sudo pkill -f 'celery -A news_app beat'
sleep 5
#changing to the newsapp folder/directory
cd /home/ubuntu/newsapp/
# activate virtual environment
python3 -m venv newsapp
source newsapp/bin/activate
# installing the requirements
pip install -r /home/ubuntu/newsapp/requirements.txt
#running migration
python3 manage.py migrate