#/usr/bin/env python2
#author: mp

import socket
import base64
import re
import sys

domain = []
wait = 0
smtp = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
smtp.connect(( sys.argv[1], 25 ))
while True:
    data = smtp.recv( 4096 )
    if "220" in data:
        smtp.send( "EHLO lol.com\r\n" )
    
    wait += 1
    if wait is 2:
        smtp.send( "AUTH NTLM\r\n" )
    
    if "334" in data:
        smtp.send( "TlRMTVNTUAABAAAAt4II4gAAAAAAAAAAAAAAAAAAAAAFAs4OAAAADw==\r\n" )
    
    if "334 T" in data:
        blob = data.split( " " )[1]
        break

for i in re.split( r'[^\w]', base64.b64decode( blob ) ):
    domain.append( i )

print "".join( char for char in domain )
