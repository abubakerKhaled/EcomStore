from decouple import config
from celery import Celery


# set the default Django settings module for the celery's program
config('DJANGO_SETTINGS_MODULE', default='ecomstore.settings')

app = Celery('ecomstore')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()