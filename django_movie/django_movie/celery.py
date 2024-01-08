import os
from datetime import datetime

from celery import Celery
from celery.schedules import crontab



app = Celery('django_movie', broker='redis://localhost:6379/0')
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_movie.settings')

app = Celery('django_movie')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app = Celery('django_movie', broker='redis://localhost:6379/0')
app.conf.beat_schedule = {
    'print_time_task': {
        'task': 'movie.tasks.print_time_task',
        'schedule': 7.0
    },
}
app.conf.beat_schedule = {
    'go_binance': {
        'task': 'movie.tasks.go_binance',
        'schedule': 10.0
    },
}





# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')