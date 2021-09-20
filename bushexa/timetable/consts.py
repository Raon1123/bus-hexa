# 상수들을 저장하는 파일
from datetime import datetime
from pytz import timezone, utc

def get_week():
    weekday = datetime.now(timezone('Asia/Seoul')).weekday()
    if weekday < 5:
        week = 0
    elif weekday == 6:
        week = 1
    else:
        week = 2

    return week


def get_now():
    timenow = datetime.now(timezone('Asia/Seoul'))

    hour = timenow.hour
    minute = timenow.now().minute
    now = str(hour).zfill(2) + str(minute).zfill(2)

    return now


def get_stop_list():
    stops = ['196040234']
    return stops


def get_bus_list(key='196040234'):
    if type(key) is not str:
        key = str(key)

    bus_dict = {'196040234':[['133','2'],['733','2'],['743','2']]}

    if key in bus_dict.keys():
        bus_list = bus_dict[key]
    else:
        bus_list = []

    return bus_list