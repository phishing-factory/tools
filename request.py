import socket
import ssl
import sys
import re

method  = sys.argv[1]
target  = sys.argv[2]
http_p  = re.match( r"^http://(.+):(.+)$", target )
https_p = re.match( r"^https://(.+):(.+)$", target )
http    = re.match( r"^http://(.+)$", target )
https   = re.match( r"^https://(.+)$", target )
sock    = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

def request( sock, method ):
    try:
        sock.send( "{} / HTTP/1.0\r\n\r\n".format( method ) )
        print sock.recv( 4096 )
        sock.close()
    except Exception as E:
        print E

if http_p:
    print "Trying connection to {} on port {}".format( http_p.group( 1 ), http_p.group( 2 )  )
    sock.connect(( http_p.group( 1 ), int( http_p.group( 2 ) ) ))
    request( sock, method )

elif https_p:
    print "Trying connection to {} on port {}".format( https_p.group( 1 ), https_p.group( 2 ) )
    sock.connect(( https_p.group( 1 ), int( https_p.group( 2 ) ) ))
    ssl = ssl.wrap_socket( sock )
    request( ssl, method )

elif http:
    print "Trying connection to {}".format( http.group( 1 ) )
    sock.connect(( http.group( 1 ), 80 ))
    request( sock, method )

elif https:
    print "Trying connection to {}".format( https.group( 1 ) )
    sock.connect(( https.group( 1 ), 443 ))
    ssl = ssl.wrap_socket( sock )
    request( ssl, method )
