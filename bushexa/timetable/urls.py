from django.urls import path

from . import views

appname = 'timetable'
urlpatterns = [
    path('', views.timeshow, name='index'),
    path('busno/', views.busnoshow, name='busno'),
]