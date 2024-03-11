#!/bin/bash
#changing the directory
cd /home/ubuntu/newsapp/
# activate virtual environment
source newsapp/bin/activate
# run server in background
screen -d -m python3 manage.py runserver
#sleep command
sleep 5
# nginx reload
sudo systemctl reload nginx
# running celery in background
celery -A news_app beat -l info > /tmp/deploy.log 2>&1 &

celery -A news_app worker --loglevel=info  > /tmp/deploy1.log 2>&1 &
