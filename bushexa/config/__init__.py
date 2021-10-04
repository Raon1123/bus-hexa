from .celery import app as celery_app


# Make sure celery app is always imported when django starts
__all__ = ('celery_app',)
