from django.db import models

# Create your models here.

"""
Class of Bustimetable
- bus_no: bus number eg) 133
- bus_dir: direction of bus
- bus_week: week type of timetable
- bus_time: arrival time
"""
class BusTimetable(models.Model):
    bus_no = models.IntegerField(default=0)
    bus_dir = models.IntegerField(default=0)
    bus_week = models.IntegerField(default=0)

    bus_time = models.CharField(max_length=4)

    def __str__(self):
        return str(self.bus_no)


class ArrivalInfo(models.Model):
    stop_id = models.IntegerField(default=196040234)

    vehicle_no = models.CharField(max_length=16)
    route_id = models.IntegerField(default=9999)

    remain_time = models.IntegerField(default=9999)
    stop_cnt = models.IntegerField(default=9999)
    stop_name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.route_id)