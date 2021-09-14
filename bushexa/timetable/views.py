from django.shortcuts import render
from django.http import HttpResponse

from .models import BusTimetable

# Create your views here.
def index(request):
    return HttpResponse("Hello Django")

def tableshowid(request, request_id):
    response = "The time of request id %s."
    tl = BusTimetable.objects.filter(bus_no=request_id, bus_time__gt="0900")[:10]
    time = ', '.join([q.bus_time for q in tl])
    return HttpResponse(response % time)