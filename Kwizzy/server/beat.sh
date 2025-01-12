export TZ=Asia/Kolkata
celery -A backend.celery beat --loglevel=INFO