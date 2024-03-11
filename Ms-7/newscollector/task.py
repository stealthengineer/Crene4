from celery import shared_task
from .scripts.newsapi import DataCollector
from .scripts.newsapi_nytimes import getdata_nytimes
from .scripts.newsapi_mediastack import get_ms_data
from newscollector.utils import insert_to_db

@shared_task(bind=True)
def news_scrapper(self):
    try:
        ny_data = getdata_nytimes()
        insert_to_db(ny_data)
    except Exception as e:
        print(e)
    try:
        nws_data = DataCollector().main()
        insert_to_db(nws_data)
    except Exception as e:
        print(e)   
    try:
        ms_data = get_ms_data()
        insert_to_db(ms_data)
    except Exception as e:
        print(e)
    return "done"

