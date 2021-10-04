import os

from celery import Celery
from datetime import timedelta

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

"""
app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'update-every-second': {
            'task': 'chroniccrawler.tasks.printtest',
            'schedule': timedelta(seconds=2),
            'args': ()
        },
    }
)
"""

# Test task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
