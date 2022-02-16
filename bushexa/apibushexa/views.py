from django.shortcuts import render
from django.http import JsonResponse

from .helper import get_busno as get_busno


def api_get_busno(request):
    return JsonResponse(
        {
            "arrival": get_busno.get_all_arrival(),
            "position": {
                "tbi": ["tbi", "tbi", "tbi"],
            },
            "departure": {
                "tbi": "tbi",
            }
        })
