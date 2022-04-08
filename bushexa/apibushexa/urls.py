from django.urls import path

from . import views

appname = 'apibushexa'

urlpatterns = [
    path('apibushexa/busno/', views.api_get_busno, name='apibusno'),
    path('apibushexa/lane/<int:db_lane_id>', views.api_get_onelane, name='apionelane'),
]
