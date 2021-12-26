from django.contrib import admin

from .models import LaneToTrack, UlsanBus_LaneToTrack, NodeOfLane, PosOfBus, UlsanBus_TimeTable, DayInfo, UlsanBus_NodeToTrack, UlsanBus_ArrivalInfo, LaneAlias, LanePart

admin.site.register(LaneToTrack)
admin.site.register(NodeOfLane)
admin.site.register(PosOfBus)

admin.site.register(LaneAlias)
admin.site.register(LanePart)

admin.site.register(DayInfo)

admin.site.register(UlsanBus_LaneToTrack)
admin.site.register(UlsanBus_TimeTable)
admin.site.register(UlsanBus_NodeToTrack)
admin.site.register(UlsanBus_ArrivalInfo)
