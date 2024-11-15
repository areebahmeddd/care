web: gunicorn config.wsgi:application
release: python manage.py collectstatic --noinput && python manage.py migrate
worker: celery -A config.celery_app worker --loglevel=info
beat: celery -A config.celery_app beat --loglevel=info
