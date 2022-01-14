from typing import Any, Dict
from django.shortcuts import redirect
# from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import TemplateResponseMixin
from .tools.tools import *
from .tools.helpers import *

from chroniccrawler import *


class TimeTableMixin:
    """
    시간 기준으로 버스 목록 표시
    """
    def get_timetable_context(self) -> Dict[str, Any]:
        now = get_now()
        bus_time = get_bustime(now)
        return {
            'request_time': pretty_time(now),
            'time_table': bus_time,
        }

class TimeBasedBusListView(TemplateView, TimeTableMixin):

    template_name = "timetable/departure.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.get_timetable_context())
        return context

class BusInfoMixin:
    STOP_ID = "196040234"

    """
    버스 번호 기준으로 표시
    """
    def get_businfo_context(self) -> Dict[str, Any]:
        # crawl_arrival() # 추후 API에 직접 요청하는 부분을 삭제할것 **FIXIT**

        bus_info = get_busstop_time(self.STOP_ID)
        stop_name = get_stop_string(self.STOP_ID)
        return {
            'stop_name': stop_name,
            'bus_info': bus_info
        }

class BusNumberBasedBusListView(TemplateView, BusInfoMixin):

    template_name = "timetable/busno.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.get_businfo_context())
        return context


class AliasToIndividualBusView(DetailView, TemplateResponseMixin):

    model = LaneAlias
    context_object_name = 'alias'
    template_name = "timetable/alias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lanes = {'lanes': MapToAlias.objects.filter(alias_key=context['alias'])\
                                            .select_related('lane_key')\
                                            .values('lane_key', 'lane_key__bus_name')}
        context.update(lanes)
        return context


class IndividualLaneView(DetailView, TemplateResponseMixin):

    model = LaneToTrack
    context_object_name = 'lane'
    template_name = "timetable/lane.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nodes = {'nodes': NodeOfLane.objects.filter(route_key=context['lane'])}
        tts = UlsanBus_TimeTable.objects.filter(route_key_usb__route_key=context['lane'])
        timetables = {'timetables': [{'hour': tt.depart_time[:2], 'minute': tt.depart_time[2:],} for tt in tts],}
        context.update(nodes)
        context.update(timetables)
        return context


def index(request):
    return redirect('busno')
