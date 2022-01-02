from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


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
        return "Lane " + self.route_key.bus_name + " " + self.node_id + " - " + \
               self.node_name + ", order " + str(self.node_order)

# Data from 국토교통부
class PosOfBus(models.Model):
    route_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=20)
    bus_num = models.CharField(max_length=20)
    node_order = models.IntegerField()

    def __str__(self):
        return "lane " + self.route_key.bus_name + " : " + self.bus_num + " on node " + str(self.node_order)


# Data from 한국천문연구원
class DayInfo(models.Model):
    year = models.CharField(max_length=5)
    month = models.CharField(max_length=3)
    day = models.CharField(max_length=3)
    # kind : 0==normal 1==saturday 2==holiday(national, sunday)
    name = models.CharField(max_length=64)
    kind = models.IntegerField()

    def __str__(self):
        ymd = self.year + "년 " + self.month + "월 " + self.day + "은 "
        return ymd + self.name

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

# Data from 울산광역시 BIS
class UlsanBus_NodeToTrack(models.Model):
    node_name = models.CharField(max_length=40)
    node_id = models.CharField(max_length=20)

    def __str__(self):
        return "Tracking bus stop " + self.node_id + " : " + self.node_name

# Data from 울산광역시 BIS
class UlsanBus_ArrivalInfo(models.Model): 
    route_key_usb = models.ForeignKey(UlsanBus_LaneToTrack, on_delete=models.CASCADE)
    node_key_usb = models.ForeignKey(UlsanBus_NodeToTrack, on_delete=models.CASCADE)
    prev_stop_cnt = models.IntegerField()
    arrival_time = models.IntegerField()
    vehicle_no = models.CharField(max_length=20, unique=True)
    current_node_name = models.CharField(max_length=40)
    

    def __str__(self):
        return str(self.prev_stop_cnt) + " stop(s) left, estimated arrival time " + str(self.arrival_time)


# Alias for track
class LaneAlias(models.Model):
    alias_name = models.CharField(max_length=60)

    def __str__(self):
        return "Alias " + self.alias_name


# Part for lanes
class PartOfLane(models.Model):
    lane_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    first_node_key = models.ForeignKey(NodeOfLane, on_delete=models.CASCADE, related_name="fnk")
    last_node_key = models.ForeignKey(NodeOfLane, on_delete=models.CASCADE, related_name="lnk")
    part_name = models.CharField(max_length=60)
    count = models.IntegerField()

    def __str__(self):
        return self.part_name

    def only_departure(self):
        if self.first_node_key == self.last_node_key and self.first_node_key.node_order == 1:
            return True
        else:
            return False

    def in_part(self, buspos):
        if buspos.route_key == self.lane_key:
            if self.first_node_key.node_order <= buspos.node_order \
                and self.last_node_key.node_order > buspos.node_order:
                return True
        return False


# Map each part of lane to alias
class MapToAlias(models.Model):
    lane_key = models.ForeignKey(LaneToTrack, on_delete=models.CASCADE)
    count = models.IntegerField()
    alias_key = models.ForeignKey(LaneAlias, on_delete=models.CASCADE)

    def __str__(self):
        return "Map count " + str(self.count) + " of " + self.lane_key.route_id + " to " + self.alias_key.alias_name


