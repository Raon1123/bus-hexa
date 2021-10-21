from celery import shared_task

from .crawler.laneinfo import do_laneinfo
from .crawler.buspos import do_buspos
from .crawler.timetable_usb import do_timetable
from .crawler.dayinfo import do_dayinfo
from .crawler.arrivalinfo import do_arrivalinfo

from .models import DayInfo


@shared_task
def get_lane_info():
    do_laneinfo()


@shared_task
def get_bus_pos():
    do_buspos()


@shared_task
def get_time_table():
    dayInfo = DayInfo.objects.first()
    if dayInfo == None:
        return
    do_timetable(dayInfo.kind)


@shared_task
def get_day_info():
    do_dayinfo()


@shared_task
def get_arrival_info():
    do_arrivalinfo()


@shared_task
def printtest():
    print('hello world!')
