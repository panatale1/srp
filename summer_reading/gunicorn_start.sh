#!/bin/bash

NAME="timeclock"
DJANGODIR=/home/peter/repos/srp/summer_reading
SOCKFILE=/home/peter/repos/srp/run/gunicorn.sock
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=summer_reading.settings
DJANGO_WSGI_MODULE=summer_reading.wsgi

# Activate virtualenv
cd $DJANGODIR
WRAPPER_PATH=$(which virtualenvwrapper.sh)
source $WRAPPER_PATH
workon summer_reading 
echo "$DJANGODIR"
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
echo "$RUNDIR"
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
	--name $NAME \
	--workers $NUM_WORKERS \
	--bind=unix:$SOCKFILE \
	#--bind 127.0.0.1:8000
	--log-leve=debug \
	--log-file=-
