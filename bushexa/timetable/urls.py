from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:request_time>/', views.timetableshow, name='timeshow'),
]