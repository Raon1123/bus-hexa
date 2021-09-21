from django.urls import path

from . import views

appname = 'timetable'
urlpatterns = [
    path('', views.index, name='index'),
    path('departure/', views.timeshow, name='departure'),
    path('busno/', views.busnoshow, name='busno'),
]