from django.apps import AppConfig
from django.conf import settings

class TimetableConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD
    name = 'timetable'
