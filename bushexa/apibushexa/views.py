from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from chroniccrawler.models import *
from .helper import get_busno, get_onelane, get_lanes, get_onealias


def api_get_busno(request):
    return JsonResponse(get_busno.build_response_dict())


def api_get_onelane(request, db_lane_id):
    lane = get_object_or_404(LaneToTrack, pk=db_lane_id)
    return JsonResponse(get_onelane.build_response_dict(lane))


def api_get_lanes(request):
    return JsonResponse(get_lanes.build_response_dict())


def api_get_onealias(request, db_alias_id):
    alias = get_object_or_404(LaneAlias, pk=db_alias_id)
    return JsonResponse(get_onealias.build_response_dict(alias))
