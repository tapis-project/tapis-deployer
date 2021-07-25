#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/home/tapis
#cd /home/tapis/service; /usr/local/bin/gunicorn --log-file=- -w $threads -b :5000 api:app
cd /home/tapis/service; /usr/local/bin/gunicorn --log-file= -k $workerCls -w $processes -b :5000 api:app

while true; do sleep 86400; done
