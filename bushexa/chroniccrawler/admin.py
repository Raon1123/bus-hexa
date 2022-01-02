from django.contrib import admin

from .models import *

admin.site.register(LaneToTrack)
admin.site.register(NodeOfLane)
admin.site.register(PosOfBus)

admin.site.register(LaneAlias)
admin.site.register(PartOfLane)
admin.site.register(MapToAlias)

admin.site.register(DayInfo)

admin.site.register(UlsanBus_LaneToTrack)
admin.site.register(UlsanBus_TimeTable)
admin.site.register(UlsanBus_NodeToTrack)
admin.site.register(UlsanBus_ArrivalInfo)

admin.site.register(LandmarkAlias)
admin.site.register(LandmarkNode)
admin.site.register(LandmarkOfLane)
