from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *

from chroniccrawler.models import *


class LaneToTrackViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = LaneToTrack.objects.all()
        serializer = LaneToTrackSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = LaneToTrack.objects.all()
        lane = get_object_or_404(queryset, pk=pk)
        serializer = LaneToTrackSerializer(lane)
        return Response(serializer.data)


class NodeOfLaneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NodeOfLane.objects.all()
    serializer_class = NodeOfLaneSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['route_key']


class PosOfBusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PosOfBus.objects.all()
    serializer_class = PosOfBusSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['route_key', 'bus_num']


class UlsanBus_LaneToTrackViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UlsanBus_LaneToTrack.objects.all()
    serializer_class = UlsanBus_LaneToTrackSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['route_key']


class UlsanBus_TimeTableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UlsanBus_TimeTable.objects.all()
    serializer_class = UlsanBus_TimeTableSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['route_key_usb']


class UlsanBus_NodeToTrackViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UlsanBus_NodeToTrack.objects.all()
    serializer_class = UlsanBus_NodeToTrackSerializer


class UlsanBus_ArrivalInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UlsanBus_ArrivalInfo.objects.all()
    serializer_class = UlsanBus_ArrivalInfoSerializer
    filter_fields = ['route_key_usb', 'node_key_usb', 'vehicle_no']


class LaneAliasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LaneAlias.objects.all()
    serializer_class = LaneAliasSerializer
    filter_fields = []


class PartOfLaneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PartOfLane.objects.all()
    serializer_class = PartOfLaneSerializer
    filter_fields = ['lane_key', 'count']


class MapToAliasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapToAlias.objects.all()
    serializer_class = MapToAliasSerializer
    filter_fields = ['lane_key', 'count', 'alias_key']


class LandmarkAliasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandmarkAlias.objects.all()
    serializer_class = LandmarkAliasSerializer
    filter_fields = []


class LandmarkNodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandmarkNode.objects.all()
    serializer_class = LandmarkNodeSerializer
    filter_fields = ['alias_key', 'node_id']


class LandmarkOfLaneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandmarkOfLane.objects.all()
    serializer_class = LandmarkOfLaneSerializer
    filter_fields = ['route_key']
