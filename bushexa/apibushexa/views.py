from django.shortcuts import render
from django.http import JsonResponse

from .helper import get_busno as get_busno


def api_get_busno(request):
    return JsonResponse(get_busno.build_response_dict())
