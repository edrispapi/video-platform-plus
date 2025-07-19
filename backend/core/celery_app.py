import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.video_platform.settings') # مسیر کامل به settings.py

app = Celery('video_platform') # نام پروژه اصلی Django

# استفاده از تنظیمات Celery از Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# کشف خودکار وظایف از فایل‌های tasks.py در اپلیکیشن‌های Django
app.autodiscover_tasks()
