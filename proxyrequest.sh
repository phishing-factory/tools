#!/bin/bash
#author: mp
#comment: simple command for doing DNS lookups over a socks proxy
#         requires proxychains to be installed
usage () {
  echo "./proxydns RECORD domain.com"
  exit 1
}

[ -z $1 ] && usage
[ -z $2 ] && usage

export LD_PRELOAD=libproxychains.so.3
dig @4.2.2.2 $1 $2 +short +tcp
