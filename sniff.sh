#!/bin/bash
#author: mp
#comment: poor mans sniffer

proto=""

usage() {
    echo "usage: $0 -s <proto>"
    echo "protocol options:"
    echo "  http"
    echo "  ftp - coming soon"
    echo "  telnet - comming soon"
    echo "  smtp - comming soon"
    echo "  irc - coming soon"
    exit 1
}

while [ -n "$1" ] ; do 
    case "$1" in
        -s)
            shift; proto="$1";;
        -u)
            shift; int="$1";;
        *)
            echo "invalid switch"
            usage;;
    esac ; shift
done

[ -z "$proto" ] && usage
if [[ $proto == *"http"* ]] ; then
    stdbuf -oL -eL tcpdump -A -s 10240 "tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)" | egrep -a --line-buffered ".+(GET |HTTP\/|POST )|^[A-Za-z0-9-]+: " | perl -nle 'BEGIN{$|=1} { s/.*?(GET |HTTP\/[0-9.]* |POST )/\n$1/g; print }' | while read line ; do 
        #All Methods are black on blue 
        if [[ $line == *"OPTIONS"* ]] ; then 
            echo -e '\E[30;44m'"$line\033[0m" 
        elif [[ $line == *"GET"* ]] ; then 
            echo -e '\E[30;44m'"$line\033[0m"
        elif [[ $line == *"HEAD"* ]] ; then
            echo -e '\E[30;44m'"$line\033[0m"
        elif [[ $line == *"PUT"* ]] ; then
            echo -e '\E[30;44m'"$line\033[0m"
        elif [[ $line == *"DELETE"* ]] ; then
            echo -e '\E[30;44m'"$line\033[0m"
        elif [[ $line == *"TRACE"* ]] ; then
            echo -e '\E[30;44m'"$line\033[0m"
        elif [[ $line == *"CONNECT"* ]] ; then
            echo -e '\E[30;44m'"$line\033[0m"
        #Status codes vary
        elif [[ $line == *"HTTP/1.1 2"* ]] ; then
            echo -e '\E[30;42m'"$line\033[0m" #20X Success black on green
        elif [[ $line == *"HTTP/1.1 3"* ]] ; then
            echo -e '\E[30;45m'"$line\033[0m" #3XX Redirection black on magenta
        elif [[ $line == *"HTTP/1.1 4"* ]] ; then
            echo -e '\E[30;43m'"$line\033[0m" #4XX Client error black on yellow 
        elif [[ $line == *"HTTP/1.1 5"* ]] ; then
            echo -e '\E[37;41m'"$line\033[0m" #5XX Server error white on red
        #Common headers are cyan
        elif [[ $line == *":"* ]] ; then
            echo -e '\E[1;36m'"$line\033[0m"
        #Everything else just plain
        else
            echo $line
        fi
    done
fi