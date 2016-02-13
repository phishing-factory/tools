#!/usr/bin/env python2
#author: mp
#comment: verify a list of emails using the RCPT TO method
#you will probably have to change a lot of this
#converation before running as some mail servers
#dont follow the spec.

import socket
import sys

sock  = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.connect(( "smtp.example.com", 25 ))
        
while True:
    data = sock.recv( 4096 )
    if "ESMTP" in data: #data before sending EHLO
        sock.send( "EHLO lol.com\r\n" )
    if "SMTPUTF8" in data: #last line after EHLO
        sock.send( "MAIL FROM:<noone@gmail.com>\r\n" )
    if "250 2.1.0 OK" in data:
        for email in open( sys.argv[1], "r" ):
            """ check response for each email """
            email = email.rstrip( "\n" )
            sock.send( "RCPT TO:<{}>\r\n".format( email ) )
            data = sock.recv( 4096 )
            if "250" in data:
                print "\033[1;32m[+]\033[1;m Valid: {}".format( email )
            elif "550" in data:
                print "\033[1;31m[!]\033[1;m Invalid: {}".format( email )
            else:
                print "\033[1;34[-]\033[1;m Fucked up"
        break

sock.close()
