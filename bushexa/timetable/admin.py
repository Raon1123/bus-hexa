from django.contrib import admin

from .models import BusTimetable, ArrivalInfo

# Register your models here.
admin.site.register(BusTimetable)
admin.site.register(ArrivalInfo)