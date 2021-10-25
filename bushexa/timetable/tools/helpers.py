from timetable.models import ArrivalInfo, BusTimetable
from chroniccrawler.models import *
import datetime

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
    ans = []
    aliases = LaneAlias.objects.all()
    for alias in aliases:
        time_things = []
        busname = alias.alias_name
        parts = LanePart.objects.filter(alias_key=alias)
        for part in parts:
            usb = UlsanBus_LaneToTrack.objects.get(route_key=part.lane_key)
            arrival = UlsanBus_ArrivalInfo.objects.filter(route_key_usb=usb)
            count = 0
            if len(arrival) != 0:
                time_things.append({'remain_time': str(int(int(arrival[0].arrival_time)/60))+'분 후',
                                    'stop_name': arrival[0].current_node_name})
                count = count + 1
            new = UlsanBus_TimeTable.objects.filter(route_key_usb=usb)
            now = datetime.now()
            for onetime in new:
                h = int(onetime.depart_time[0:2])
                m = int(onetime.depart_time[2:4])
                if count >= 2:
                    break
                if h > now.hour or (h == now.hour and m >= now.minute):
                    count = count + 1
                    until = str(((h-now.hour)*60+m-now.minute)*60)
                    time_things.append({'bus_time': onetime.depart_time[0:2]+':'+onetime.depart_time[2:4]})
        while len(time_things) < 2:
            time_things.append({'no_data': 'No_data'})
        ans.append({'bus_name': busname, 'stop_info': time_things[0:2]})
    
    print(ans)
    return ans
