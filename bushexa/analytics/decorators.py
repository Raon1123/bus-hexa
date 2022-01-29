import datetime
from django.db.models import F

from analytics.models import *


def track_hourly_load(func):
    def wrap(request, *args, **kwargs):
        now = datetime.datetime.now()
        path = request.path
        obj, created = HourlyLoad.objects.get_or_create(
            date=now.date(), hour=now.hour, path=path, defaults={'load': 0},
        )

        obj.load = F('load') + 1
        obj.save()

        return func(request, *args, **kwargs)
    return wrap
