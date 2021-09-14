from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:request_id>/', views.tableshowid, name='showid'),
]