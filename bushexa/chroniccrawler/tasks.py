from celery import shared_task

from .crawler.laneinfo import do_laneinfo


@shared_task
def get_lane_info():
    do_laneinfo()


@shared_task
def printtest():
    print('hello world!')
