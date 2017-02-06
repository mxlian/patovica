#!/bin/bash
# 
# DISCLAIMER: This is just a proof of concept
#   For god sake, I'm using the IP of the phone!
#
OPENDOR_BIN="python ./opendoor.py"
PING_DEBUG=/tmp/pingdebug.log
CELLPHONE_IP=192.168.1.54

echo "$(date): will wait until the pone goes away"
while true; do
    ((count = 4))                
    while [[ $count -ne 0 ]] && ! ping -c1 $CELLPHONE_IP >$PING_DEBUG; do
        ((count = count - 1)) 
        sleep 1
        echo "$count"
    done
    
    if [[ "$count" -ne 0 ]]; then
        #echo "$(date): still active, restarting"
        sleep 1
        continue
    fi

    echo "$(date): long time gone, if appears i will open it right away"
    while ! ping -c1 $CELLPHONE_IP >$PING_DEBUG; do
        sleep 1
    done

    echo "$(date): found, calling servo control..."
    $OPENDOR_BIN
done
