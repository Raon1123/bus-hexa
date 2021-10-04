from django.shortcuts import render, redirect
# from django.http import HttpResponse, JsonResponse

from .tools.tools import *
from .tools.helpers import *

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

    crawl_arrival() # 추후 API에 직접 요청하는 부분을 삭제할것 **FIXIT**

    bus_info = get_busstop_time(stop_id)

    stop_name = get_stop_string(stop_id)
    
    context = {
        'stop_name': stop_name,
        'bus_info': bus_info
    }

    return render(request, 'timetable/busno.html', context)    


def index(request):
    return redirect('busno')