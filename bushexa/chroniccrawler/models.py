from django.db import models


class LaneToTrack(models.Model):
    bus_name = models.CharField(max_length=30)
    route_id = models.CharField(max_length=20)
    city_code = models.CharField(max_length=10)

    def __str__(self):
        return self.bus_name + " : " + self.route_id

class NodeOfLane(models.Model):
    route_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    node_order = models.IntegerField()
    node_id = models.CharField(max_length=20)
    node_name = models.CharField(max_length=40)

    def __str__(self):
        return self.node_id + " - " + self.node_name + ", order " + str(self.node_order)

class PosOfBus(models.Model):
    route_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=20)
    bus_num = models.CharField(max_length=20)
    node_order = models.IntegerField()
