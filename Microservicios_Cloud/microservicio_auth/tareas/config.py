from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')
celery_app.conf.update(result_backend='redis://localhost:6379/0')