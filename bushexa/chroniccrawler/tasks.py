from celery import shared_task

from .crawler.laneinfo import do_laneinfo
from .crawler.buspos import do_buspos
from .crawler.timetable_usb import do_timetable


@shared_task
def get_lane_info():
    do_laneinfo()


@shared_task
def get_bus_pos():
    do_buspos()


@shared_task
def get_time_table(dayOfWeek):
    do_timetable(dayOfWeek)


@shared_task
def printtest():
    print('hello world!')
