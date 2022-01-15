from django.urls import path

from . import views

appname = 'timetable'
urlpatterns = [
    path('', views.index, name='index'),
    path('departure/', views.TimeBasedBusListView.as_view(), name='departure'),
    path('busno/', views.BusNumberBasedBusListView.as_view(), name='busno'),
    path('alias/<pk>', views.AliasToIndividualBusView.as_view(), name='alias'),
    path('lane/<pk>', views.IndividualLaneView.as_view(), name='indlane'),
    path('lanes/', views.AllLanesView.as_view(), name='lanes'),
]
