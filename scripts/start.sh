#!/bin/bash
printf "api" > /tmp/container-role

set -eo pipefail

if [ -z "${DATABASE_URL}" ]; then
  export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
fi

if [ -z "${REDIS_URL}" ]; then
  export REDIS_URL="rediss://:${REDIS_AUTH_TOKEN}@${REDIS_HOST}:${REDIS_PORT}/${REDIS_DATABASE}?ssl_cert_reqs=none"
fi


./wait_for_db.sh
./wait_for_redis.sh

python manage.py collectstatic --noinput
python manage.py compilemessages -v 0

export NEW_RELIC_CONFIG_FILE=/etc/newrelic.ini
if [[ -f "$NEW_RELIC_CONFIG_FILE" ]]; then
  newrelic-admin run-program gunicorn --config python:config.gunicorn config.wsgi:application --bind 0.0.0.0:9000 --chdir=/app
else
  gunicorn --config python:config.gunicorn config.wsgi:application --bind 0.0.0.0:9000 --chdir=/app --workers 2
fi
