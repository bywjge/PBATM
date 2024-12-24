#!/bin/bash  
log_file="/home/ubuntu/crontab_output.log"



step=5  # 间隔的秒数，5秒
for (( i = 0; i < 60; i=(i+step) )); do  
    python3 /home/ubuntu/Crawler.py >> $log_file 2>&1
    sleep $step  # 每次等待5秒
done  
exit 0
