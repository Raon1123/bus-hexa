from django.urls import path

from . import views

appname = 'timetable'
urlpatterns = [
    path('', views.index, name='index'),
    path('departure/', views.TimeBasedBusListView.as_view(), name='departure'),
    path('busno/', views.BusNumberBasedBusListView.as_view(), name='busno'),
]