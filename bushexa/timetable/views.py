from datetime import datetime
from pytz import timezone, utc

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import BusTimetable

from .consts import *

bus_list = [133, 733, 743]

# Create your views here.
"""

"""
def index(request):
    # Calculate current weekday and time
    week = get_week()
    now = get_now()

    timetable = {}

    for bus in bus_list:
        bus_timetable = BusTimetable.objects.filter(bus_no__exact=bus,
                                                    bus_week=week, 
                                                    bus_time__gte=now)[:5]
        bus_time_list = [str(b.bus_time) for b in bus_timetable]
        timetable[str(bus)] = bus_time_list

    context = {
        'weekday': week,
        'requestTime': now,
        'timetable': timetable
    }
    
    # return JsonResponse(context)
    return render(request, 'timetable/index.html')


def timetableshow(request, request_time):
    buses = get_bus_list()
    week = get_week()

    bus_time = []

    for bus_no, dir in buses:
        times = BusTimetable.objects.filter(bus_no__exact=bus_no,
                                            bus_dir__exact=dir,
                                            bus_week=week,
                                            bus_time__gte=request_time)[:2]
        for time in times:
            time_dict = [bus_no, time.bus_time]
            bus_time.append(time_dict)
    
    context = {'timeTable': bus_time}

    return render(request, 'timetable/index.html', context)
    # return JsonResponse(context)