from django.contrib import admin

from .models import LaneToTrack
from .models import NodeOfLane

admin.site.register(LaneToTrack)
admin.site.register(NodeOfLane)
