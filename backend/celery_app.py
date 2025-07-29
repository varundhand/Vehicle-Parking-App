from celery import Celery
from celery.schedules import crontab

# Create Celery instance
celery_app = Celery(
    'parking_app',
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0',
    include=['tasks.email_tasks']  # Include task modules
)

# Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Configure periodic tasks (Celery Beat schedule)
celery_app.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'tasks.email_tasks.send_daily_reminders',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9 AM
    },
    'monthly-reports': {
        'task': 'tasks.email_tasks.send_monthly_reports',
        'schedule': crontab(day_of_month='1', hour=10, minute=0),  # 1st of every month at 10 AM
    },
}

if __name__ == '__main__':
    celery_app.start()