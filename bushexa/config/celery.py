import os

from celery import Celery, chain, group
from celery.signals import beat_init, celeryd_init, celeryd_after_setup
from datetime import timedelta
from celery.schedules import crontab


# Set Default django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config', broker='amqp://guest@localhost:5672//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
)
# Load task modules from other django apps
app.autodiscover_tasks()


'''
# Run tasks in such order when Celery starts
@celeryd_init.connect
def on_start_celery(**k):
    # Clear task queue
    app.control.purge()

    # Do required tasks on startup
    from chroniccrawler.tasks import get_day_info, get_lane_info, get_time_table
    result = chain(get_day_info.si(), get_lane_info.si(), get_time_table.si())()
    while result.ready():
        pass

    return
'''

# Daily tasks chained together
@app.task
def daily_tasks():
    from chroniccrawler.tasks import get_day_info, get_lane_info, get_time_table
    result = chain(get_day_info.si(), get_lane_info.si(), get_time_table.si())()

    return


# Run tasks in such order when Beat starts
@beat_init.connect
def on_start_beat(sender, **k):
    # Clear task queue
    app.control.purge()

    # Do required tasks on startup
    from chroniccrawler.tasks import get_day_info, get_lane_info, get_time_table, get_bus_pos, get_arrival_info 
    result = chain(get_day_info.si(), get_lane_info.si(), get_time_table.si())()
    while not result.ready():
        pass

    # Create Daily schedule and periodic task if there aren't
    from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule, CrontabSchedule
    daily_schedule, _ = CrontabSchedule.objects.get_or_create(minute='1', hour='0', 
        day_of_week='*', day_of_month='*', month_of_year='*',)
    PeriodicTask.objects.get_or_create(crontab=daily_schedule, name='Daily reloading', task='.daily_tasks')

    # Create Bus position getting schedule and periodic task if there aren't
    buspos_schedule, _ = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS,)
    PeriodicTask.objects.get_or_create(interval=buspos_schedule, 
        name='Getting bus positions', task='chroniccrawler.tasks.get_bus_pos',)
    PeriodicTask.objects.get_or_create(interval=buspos_schedule, 
        name='Getting arrival infos', task='chroniccrawler.tasks.get_arrival_info')

    return


# Test task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
