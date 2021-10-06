from django.contrib import admin

from .models import LaneToTrack, UlsanBus_LaneToTrack, NodeOfLane, PosOfBus, UlsanBus_TimeTable, DayInfo

admin.site.register(LaneToTrack)
admin.site.register(NodeOfLane)
admin.site.register(PosOfBus)

admin.site.register(DayInfo)

admin.site.register(UlsanBus_LaneToTrack)
admin.site.register(UlsanBus_TimeTable)
