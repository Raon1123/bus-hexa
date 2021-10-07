import os

from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

# Set Default django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul'
)
# Load task modules from other django apps
app.autodiscover_tasks()


# day update task every 00:01
# lane info update task every 00:01
# timetable update task every 00:02
# bus position update task every 20 seconds
app.conf.update(
    CELERYBEAT_SCHEDULE = {        
        'update-day' : {
            'task': 'chroniccrawler.tasks.get_day_info',
            'schedule': crontab(minute=1, hour=0),
            'args': ()
        },
        'update-laneinfo' : {
            'task': 'chroniccrawler.tasks.get_lane_info',
            'schedule': crontab(minute=1, hour=0),
            'args': ()
        },
        'update-timetable' : {
            'task': 'chroniccrawler.tasks.get_time_table',
            'schedule': crontab(minute=2, hour=0),
            'args': ()
        },
        'update-buspos' : {
            'task': 'chroniccrawler.tasks.get_bus_pos',
            'schedule': 20.0,
            'args': ()
        },
    }
)


'''
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Daily dayinfo loading
    sender.add_periodic_task(3.0, printtest())
    
    sender.add_periodic_task(
        crontab(hour=0),
        get_day_info()
        )
'''

# Test task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
