import os
from celery import Celery

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')

app = Celery('clothing_store')

# 从Django设置中读取Celery配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
