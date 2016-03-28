#!/bin/bash

count=0

echo "[+] Starting..."
while true; do
    sessions=$( netstat -plantu | grep ruby | grep ESTABLISHED | wc -l )
    if [[ $sessions -gt $count ]]; then
        echo "Meterpreter session opened" >/dev/tcp/45.79.144.216/4444 && echo "[+] Sent SMS"
        count=$sessions
    elif [[ $sessions -lt $count ]]; then
        count=$sessions
    fi
    sleep 1
done
