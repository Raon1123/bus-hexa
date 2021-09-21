from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import ArrivalInfo, BusTimetable

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

    # 도착정보 탐색
    route_id = '19610' + bus_no + dir
    arrival = ArrivalInfo.objects.filter(route_id__exact=route_id)

    for info in arrival:
        info_dict = {
            'remain_time': pretty_remain(info.remain_time),
            'stop_name': info.stop_name
        }
        stop_info.append(info_dict)

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

    key = bus_no + '(' + get_bus_dir(bus_no, dir) +')'
    
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


"""
시간 기준으로 버스 목록 표시
"""
def timeshow(request):
    # Calculate current weekday and time
    now = get_now()

    bus_time = get_bustime(now)

    context = {
        'request_time': pretty_time(now),
        'time_table': bus_time
    }
    
    return render(request, 'timetable/departure.html', context)

"""
버스 번호 기준으로 표시
"""
def busnoshow(request):
    stop_id = '196040234'

    crawl_arrival()

    bus_info = get_busstop_time(stop_id)

    stop_name = get_stop_string(stop_id)
    
    context = {
        'stop_name': stop_name,
        'bus_info': bus_info
    }

    return render(request, 'timetable/busno.html', context)    
    # return JsonResponse(context)


def index(request):
    return redirect('busno')