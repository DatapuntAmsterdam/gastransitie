#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x

# # collect static files
# yes yes | python manage.py collectstatic

# run uwsgi
cd /app/
exec uwsgi --static-map /gastransitie/dash/=/vue_static --static-map /gastransitie/static=/static
