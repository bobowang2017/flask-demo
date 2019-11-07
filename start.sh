#!/bin/bash
ps -aux | grep -w 5002 | awk '{print $2}' | xargs kill -9
nohup gunicorn -w 8 -b 0.0.0.0:5002 app:app -t 300 -k gevent --reload &
msg="Started Successful"
echo -e "\033[31m ${str}\033[0m"