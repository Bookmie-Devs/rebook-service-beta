#!
mkdir /var/log/celery

celery -A config  worker  --loglevel=info  -f bookmie_celery.log  --logfile=/var/log/celery/bookmie_celery.log