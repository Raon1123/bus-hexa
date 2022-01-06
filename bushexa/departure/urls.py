from django.urls import path

from . import views

appname = "departure_by_time"
urlpatterns = [
    path('departure_by_time/', views.departure_by_time, name='departure_by_time')
]
