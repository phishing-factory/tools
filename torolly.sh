#!/bin/bash
#author: mp
#comment: roll tor IPv4 every <n> seconds

seconds="$1"

usage() {
    echo "usage: ./torolly.sh <seconds>"
    exit 1
}

[ -z "$seconds" ] && usage

while true; do 
    killall -HUP tor
    echo "[$(date +"%T")] - New IPv4: $( curl -s -k https://blackcatz.org/ip )"
    sleep $seconds
done
