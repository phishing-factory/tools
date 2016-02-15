#!/usr/bin/env python2
#author: mp
#comment: verify a list of emails using SMTP VRFY

import socket
import sys
import re

if len( sys.argv ) != 2:
    print "Usage: vrfy user@server.net"
    print "       vrfy <file>"
  
def vrfy( user, host ):
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.settimeout( 3 )
    try:
        sock.connect(( host, 25 ))
        banner = sock.recv( 1024 )
        if banner is not None:
            print "Trying {}@{} :".format( user, host )
            sock.send( "VRFY" {}\r\n".format( user ) )
            result = sock.recv( 1024 )
            print "    {}".format( result )
        sock.close()
    except socket.error as E:
        print "Error :"
        print "   {}".format( E )

def check( stub ):
    user_host = re.match( r'(.+)@(.+)', stub )
    if user_host:
        vrfy( user_host.group( 1 ), user_host.group( 2 ) )
    return

check( sys.argv[1] )
