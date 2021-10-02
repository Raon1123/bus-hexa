from timetable.models import ArrivalInfo, BusTimetable

from .consts import *
from .tools import *


"""
시간 순으로 버스 목록 표출
"""
def get_bustime(request_time):
    if type(request_time) is not str:
        request_time = str(request_time)

    buses = get_bus_list()
    week = get_week()

    bus_time = []

    for bus_no, dir in buses:
        times = BusTimetable.objects.filter(bus_no__exact=bus_no,
                                            bus_dir__exact=dir,
                                            bus_week=week,
                                            bus_time__gte=request_time)[:2]
        for time in times:
            time_dict = {"bus_no": bus_no, 
                         "bus_time": pretty_time(time.bus_time),
                         "bus_dir": get_bus_dir(bus_no, dir),
                         "bus_via": get_bus_via(bus_no, dir)}
            bus_time.append(time_dict)
    
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
    bus_list = get_bus_list(request_stop)

    ans = []

    for bus_no, direction in bus_list:
        stop_dict = get_bus_arrivaltime(bus_no, direction)

        ans.append(stop_dict)

    return ans