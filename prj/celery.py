import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')

app = Celery('prj')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'parse_every_weekend': {
        'task': 'backend.tasks.parser_msk',
        'schedule': crontab(hour=8, minute=0, day_of_week='sunday'),
    },
}

app.autodiscover_tasks()
