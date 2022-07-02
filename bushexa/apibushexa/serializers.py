from rest_framework import serializers

from chroniccrawler.models import *


class LaneToTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaneToTrack
        fields = ["id", "bus_name", "route_id", "city_code"]


class NodeOfLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeOfLane
        fields = ["route_key", "node_order", "node_id", "node_name"]


class PosOfBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosOfBus
        fields = ["route_key", "node_id", "bus_num", "node_order"]


class UlsanBus_LaneToTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UlsanBus_LaneToTrack
        fields = ["id", "route_key", "route_id", "route_num", "route_direction", "route_class"]


class UlsanBus_TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UlsanBus_TimeTable
        fields = ["route_key_usb", "depart_time", "depart_seq"]


class UlsanBus_NodeToTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UlsanBus_NodeToTrack
        fields = ["node_name", "node_id"]


class UlsanBus_ArrivalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UlsanBus_ArrivalInfo
        fields = ["route_key_usb", "node_key_usb", "prev_stop_cnt", "arrival_time", "vehicle_no", "current_node_name"]


class LaneAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaneAlias
        fields = ["id", "alias_name"]


class PartOfLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOfLane
        fields = ["id", "lane_key", "first_node_key", "last_node_key", "part_name", "count"]


class MapToAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapToAlias
        fields = ["lane_key", "count", "alias_key"]


class LandmarkAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandmarkAlias
        fields = ["alias_name"]


class LandmarkNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandmarkNode
        fields = ["alias_key", "node_id"]


class LandmarkOfLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandmarkOfLane
        fields = ["route_key", "landmark_keys"]


#class (serializers.ModelSerializer):
#    class Meta:
#        model = 
#        fields = []
