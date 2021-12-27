from django.http import HttpResponse
from django.shortcuts import render

import datetime

from .forms import *
from chroniccrawler.models import UlsanBus_TimeTable

def departure_by_time(request):
    form = TimeForm()
    hour = None
    minute = None
    if request.GET.get("hour") and request.GET.get("minute"):
        form = TimeForm(request.GET)
        hour = request.GET.get("hour")
        minute = request.GET.get("minute")
    else:
        now = datetime.datetime.now()
        hour = str(now.hour)
        minute = str(now.minute)
        form = TimeForm()
        form.fields["hour"].initial = hour
        form.fields["minute"].initial = minute

    departs = UlsanBus_TimeTable.objects.all()
    

    new_departs = [[a.depart_time[:2], a.depart_time[2:], a] for a in departs if 
        int(a.depart_time[:2]) > int(hour) or (int(a.depart_time[:2]) == int(hour) and
        int(a.depart_time[2:]) >= int(minute))]

    departs = sorted(new_departs, key=lambda e: (int(e[0]), int(e[1])))

    context = {
        'form': form,
        'departs': departs,
    }

    return render(request, 'departure/get_time.html', context)
