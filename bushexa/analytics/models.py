from django.db import models

class HourlyLoad(models.Model):
    date = models.DateField()
    hour = models.IntegerField()
    load = models.IntegerField()
    path = models.CharField(max_length=64)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')+', '+str(self.hour)+', '+self.path+' : '+str(self.load)+' times'

