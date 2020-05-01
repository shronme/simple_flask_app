#! /usr/bin/env sh
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/home/code/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . $PRE_START_PATH
else
    echo "There is no script $PRE_START_PATH"
fi

# Start Supervisor, with Nginx and uWSGI
# echo "starting celery"
# celery -A celery_app.celery worker --loglevel=info
exec /usr/bin/supervisord 