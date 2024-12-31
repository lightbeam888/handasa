#!/bin/sh

if [ -z ${ENVIRONMENT} ]; then export ENVIRONMENT=local; fi

# build static assets
python /usr/src/Wagtail-CRX/manage.py collectstatic --noinput

# start api with gunicorn
/usr/src/Wagtail-CRX/virtualenv/bin/gunicorn mysite.wsgi -b 0.0.0.0:8000 --chdir=/usr/src/Wagtail-CRX
