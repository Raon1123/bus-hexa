from django.contrib import admin

from .models import LaneToTrack, NodeOfLane, PosOfBus

admin.site.register(LaneToTrack)
admin.site.register(NodeOfLane)
admin.site.register(PosOfBus)
