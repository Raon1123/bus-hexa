from django.urls import include, path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'lanetotracks', LaneToTrackViewSet, basename='lanetotracks')
router.register(r'nodeoflanes', NodeOfLaneViewSet, basename='nodeoflanes')
router.register(r'posofbuses', PosOfBusViewSet, basename='posofbuses')
router.register(r'ulsanbus_lanetotracks', UlsanBus_LaneToTrackViewSet, basename='ulsanbus_lanetotracks')
router.register(r'ulsanbus_timetables', UlsanBus_TimeTableViewSet, basename='ulsanbus_timetables')
router.register(r'ulsanbus_nodetotracks', UlsanBus_NodeToTrackViewSet, basename='ulsanbus_nodetotracks')
router.register(r'ulsanbus_arrivalinfos', UlsanBus_ArrivalInfoViewSet, basename='ulsanbus_arrivalinfos')
router.register(r'lanealiases', LaneAliasViewSet, basename='lanealiases')
router.register(r'partoflanes', PartOfLaneViewSet, basename='partoflanes')
router.register(r'maptoaliases', MapToAliasViewSet, basename='maptoaliases')
router.register(r'landmarkaliases', LandmarkAliasViewSet, basename='landmarkaliases')
router.register(r'landmarknodes', LandmarkNodeViewSet, basename='landmarknodes')
router.register(r'landmarkoflanes', LandmarkOfLaneViewSet, basename='landmarkoflanes')


urlpatterns = [
    path('', include(router.urls)),
]
