from celery.schedules import crontab
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from django.views import View
from django.contrib import messages

from .task import news_scrapper

from .scripts.newsapi import DataCollector
from .scripts.newsapi_nytimes import getdata_nytimes
from .scripts.newsapi_mediastack import get_ms_data


def add_news_data(request):
    # if request.user.is_superuser:
    # news_scrapper.delay()
    # ny_data =getdata_nytimes()   
    # nws_data = DataCollector().main()
    ms_data = get_ms_data()
    # print(ny_data)
    # print(nws_data)
    print(ms_data)
    messages.success(request, 'Data insertion started')
    # else :
    #     messages.error(request, 'You dont have permission for this tasks')
    return HttpResponseRedirect('/')

    
@staff_member_required  
def data_insertion_schedule(request):
    if request.user.is_superuser:
        try:
            time=request.POST.get('Schedule_time').split(":")
            hour=int(time[0])
            minute=int(time[1])
            schedule, created = CrontabSchedule.objects.get_or_create(hour=hour,minute = minute)
            task = PeriodicTask.objects.create(crontab=schedule, name=f"{request.POST.get('Schedule_name')}", task='newscollector.task.news_scrapper')
            messages.success(request, 'Scheduler is saved')
        except Exception as e:
            messages.error(request, str(e))
    else:
        messages.error(request, 'You dont have permission for this tasks')
    return HttpResponseRedirect('/admin')
