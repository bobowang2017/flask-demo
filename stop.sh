#!/bin/bash
ps -aux | grep -w 5002 | awk '{print $2}' | xargs kill -9
msg="Stoped Successful"
echo -e "\033[31m ${str}\033[0m"
