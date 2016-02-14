#!/bin/bash
#author: mp
#comment: Encryption algorithms: DES, Triple-DES, AES/128, AES/192 and AES/256
#Hash algorithms: MD5 and SHA1
#Authentication methods: Pre-Shared Key, RSA Signatures, Hybrid Mode and XAUTH
#Diffie-Hellman groups: 1, 2 and 5
#MODES: Aggressive and Main

TARGET=""
OUTPUT=""

declare -A ENCLIST=( ["1"]="DES" ["5"]="3DES" ["7/128"]="AES/128" ["7/192"]="AES/192" ["7/256"]="AES/256" )
declare -A HASHLIST=( ["1"]="MD5" ["2"]="SHA1" )
declare -A AUTHLIST=( ["1"]="PSK" ["2"]="RSA Signature" ["64221"]="Hybrid Mode" ["65001"]="XAUTH" )

GROUPLIST="1 2 5"
MODES="-A -M"
SUCCESS=1
VALID=""

usage() {
  echo ""
  echo "usage: $0 -t <target> -o <output>"
  echo ""
  echo "  target: target IPSec device to scan"
  echo "  output: optional text file to output to"
  echo ""
  exit 1
}


while getopts ":t:o" flags; do
  case $flags in
    t)
      TARGET="$OPTARG";;
    o)
      OUTPUT="$OPTARG";;
    \?)
      echo 'bad flag ediot'; usage;; 
  esac
done

[ -z "$TARGET" ] && echo "No target specified EDIOT" && usage


for ENC in "${!ENCLIST[@]}"; do
  for HASH in "${!HASHLIST[@]}"; do
    for AUTH in "${!AUTHLIST[@]}"; do
      for GROUP in $GROUPLIST; do
        for MODE in $MODES; do
          if [[ $MODE == *"A"* ]] ; then
            echo "[+] Attempting negotiation in Aggressive mode using the following parameters:"
          else
            echo "[+] Attempting negotiation in Main mode using the following parameters:"
          fi
          echo "     Encryption Algorithm  - ${ENCLIST["$ENC"]}"
          echo "     Hashing Algorithm     - ${HASHLIST["$HASH"]}"
          echo "     Authentication Method - ${AUTHLIST["$AUTH"]}"
          echo "     Diffie-Hellman Group  - $GROUP"
          TRANS="--trans=$ENC,$HASH,$AUTH,$GROUP"
          ike-scan $MODE $TRANS $TARGET | grep "1 returned handshake" >/dev/null && SUCCESS=1
          if [[ $SUCCESS -eq 1 ]] ; then
            echo "     >> Valid handshake returned"
            HANDSHAKE=$( echo "ike-scan $MODE $TRANS $TARGET" | sed 's/ /_/g' )
            VALID="$VALID $HANDSHAKE"
            SUCCESS=0
          fi
        done
      done
    done
  done
done

if [[ $( echo $VALID | wc -l ) -eq 0 ]] ; then
  echo "[!] No valid handshakes returned :("
  exit 1
else
  echo "[+] Valid handshakes found:"
  for i in $( echo $VALID | tr ' ' '\n' ) ; do
    line=$( echo "    $i" | sed 's/_/ /g' )
    [ ! -z "$output" ] && echo $line || echo $line | tee -a $output
  done
fi
