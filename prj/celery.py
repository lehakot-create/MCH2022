import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')

app = Celery('prj',
             include=['backend.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'parse_every_weekend': {
        'task': 'backend.tasks.parser_msk',
        'schedule': crontab(minute=0, hour='1', day_of_week='sat'),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
