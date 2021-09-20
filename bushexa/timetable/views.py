from django.shortcuts import render
from django.http import HttpResponse

from .models import BusTimetable

# Create your views here.
def index(request):
    sample_list = BusTimetable.objects.filter(bus_no=133, bus_week=0)[:5]
    context = {
        'sample_list': sample_list
    }
    return render(request, 'timetable/index.html', context)

def tableshowid(request, request_id):
    response = "The time of request id %s."
    tl = BusTimetable.objects.filter(bus_no=request_id, bus_time__gt="0900")[:10]
    time = ', '.join([q.bus_time for q in tl])
    return HttpResponse(response % time)