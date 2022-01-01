from timetable.models import ArrivalInfo, BusTimetable
from chroniccrawler.models import *
from chroniccrawler.helper.helper import next_n_bus_from_alias
import datetime

from .consts import *
from .tools import *


"""
시간 순으로 버스 목록 표출
"""
def get_bustime(request_time):
    timetables = UlsanBus_TimeTable.objects.all()

    bus_time = []

    now = datetime.now()

    for tt in timetables:
        hour = int(tt.depart_time[:2])
        minute = int(tt.depart_time[2:])
        #if hour > now.hour or (hour == now.hour and minute >= now.minute):
        time_dict = {"bus_no": tt.route_key_usb.route_num,
                         "bus_time": tt.depart_time[:2]+":"+tt.depart_time[2:],
                         "bus_dir": "placeholder",
                         "bus_via": "placeholder"}
        bus_time.append(time_dict)

    #new_bus_time = sorted(bus_time, key=lambda e)

    return bus_time


def get_bus_arrivaltime(bus_no, dir):
    week = get_week()
    now = get_now()

    stop_info = []

    key = bus_no + '(' + get_bus_dir(bus_no, dir) +')'

    # 도착정보 탐색
    route_id = '19610' + bus_no + dir
    arrival = ArrivalInfo.objects.filter(route_id__exact=route_id)

    for info in arrival:
        info_dict = {
            'remain_time': pretty_remain(info.remain_time),
            'stop_name': info.stop_name
        }
        stop_info.append(info_dict)

    if bus_no == '337':
        dir = '3'

    # 출발정보 탐색
    times = BusTimetable.objects.filter(bus_no__exact=bus_no,
                                        bus_dir__exact=dir,
                                        bus_week=week,
                                        bus_time__gte=now)[:2]

    for time in times:
        if len(stop_info) >= 2:
            break

        time_dict = {"bus_time": pretty_time(time.bus_time)}
        stop_info.append(time_dict)

    while len(stop_info) < 2:
        stop_info.append({"no_data": "No_data"})
    
    stop_dict = {
        'bus_name': key,
        'stop_info': stop_info
    }

    return stop_dict


"""
정류소에 정차하는 버스 탐색
"""
def get_busstop_time(request_stop='196040234'):
    ans = []
    aliases = LaneAlias.objects.all()
    for alias in aliases:
        ans.append(next_n_bus_from_alias(alias, 2))
    return ans
