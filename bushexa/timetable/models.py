from django.db import models

# Create your models here.

class BusTimetable(models.Model):
    bus_no = models.IntegerField(default=0)
    bus_dir = models.IntegerField(default=0)
    bus_time = models.CharField(max_length=4)

    def __str__(self):
        return str(self.bus_no)