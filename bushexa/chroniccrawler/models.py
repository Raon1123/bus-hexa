from django.db import models


# Data from 국토교통부
class LaneToTrack(models.Model):
    bus_name = models.CharField(max_length=30)
    route_id = models.CharField(max_length=20)
    city_code = models.CharField(max_length=10)

    def __str__(self):
        return self.bus_name + " : " + self.route_id

# Data from 국토교통부
class NodeOfLane(models.Model):
    route_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    node_order = models.IntegerField()
    node_id = models.CharField(max_length=20)
    node_name = models.CharField(max_length=40)

    def __str__(self):
        return self.node_id + " - " + self.node_name + ", order " + str(self.node_order)

# Data from 국토교통부
class PosOfBus(models.Model):
    route_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=20)
    bus_num = models.CharField(max_length=20)
    node_order = models.IntegerField()

    def __str__(self):
        return "lane " + self.route_key.bus_name + " : " + self.bus_num + " on node " + str(self.node_order)


# Data from 울산광역시 BIS
class UlsanBus_LaneToTrack(models.Model):
    route_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    route_id = models.CharField(max_length=20)
    route_num = models.CharField(max_length=20)
    route_direction = models.IntegerField()
    route_class = models.IntegerField()

    def __str__(self):
        return self.route_key.bus_name + " : direction " + str(self.route_direction) + " , class " + str(self.route_class)

# Data from 울산광역시 BIS
class UlsanBus_TimeTable(models.Model):
    route_key_usb = models.ForeignKey(UlsanBus_LaneToTrack, on_delete=models.CASCADE)
    depart_time = models.CharField(max_length=5)
    depart_seq = models.IntegerField()

    def __str__(self):
        return self.route_key_usb.route_key.bus_name + " number " + str(self.depart_seq) + " departing on " + self.depart_time

