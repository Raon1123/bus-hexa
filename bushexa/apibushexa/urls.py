from django.urls import path

from . import views

appname = 'apibushexa'

urlpatterns = [
    path('apibushexa/busno/', views.api_get_busno, name='apibusno'),
]
