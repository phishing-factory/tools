#!/usr/bin/env python2

import socket
from twilio.rest import TwilioRestClient

def sms( recipient, msg ):
    sid = "__INSERT__SID__HERE__"
    token = "__INSERT__TOKEN__HERE__"
    client = TwilioRestClient( sid, token )
    client.messages.create(
        to    = recipient,
        from_ = "+12262701608",
        body  = msg,
    )

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

try:
    sock.bind(( "127.0.0.1", 4444 ))
except Exception as E:
    print E
    sys.exit( 1 )

sock.listen( 10 )

while True:
    conn, addr = sock.accept()
    data = conn.recv( 4096 )
    print data
    if "Meterpreter session" and "opened" in data:
        print "[+] Sending SMS"
        sms( "__YOUR__NUMBER__HERE__", "someone ran your trojan" )
        
s.close()
