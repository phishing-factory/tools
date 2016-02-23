#!/usr/bin/env python2
#author: mp
#comment: multiprocessed socks proxy checker

from multiprocessing import Queue, Process
import argparse
import sys
import socks
import socket
import urllib2
import httplib
import signal

class SocksiPyConnection( httplib.HTTPConnection ):
    """ this is ripped from https://gist.github.com/e000/869791 typically with socks the method is to patch 
    socket before importing urllib2, however this approach would force me to unload urllib2, repatch and 
    import urllib2 all over again, this object solves this problem, thanks e000 """
    def __init__( self, proxytype, proxyaddr, proxyport=None, rdns=True, username=None, password=None, *args. **kwargs ):
        self.proxyargs  = ( proxytype, proxyaddr, proxyport, rdns, username, password )
        httplib.HTTPConnection.__init__( self, *args, **kwargs )

    def connect( self ):
        self.sock = socks.socksocket()
        self.sock.setproxy( *self.proxyargs )
        if isinstance( self.timeout, float ):
            self.sock.settimeout( self.timeout )
        self.sock.connect(( self.host, self.port ))
        
class SocksiPyHandler( urllib2.HTTPHandler ):
    """ also ripped from https://gist.github.com/e000/869791 """
    def __init__( self, *args, **kwargs ):
        self.args = args
        self.kw   = kwargs
        urllib2.HTTPHandler.__init__( self )

    def http_open( self, req ): #this seems dirty but w.e
        def build( host, port=None, strict=None, timeout=0 ):
            conn = SocksiPyConnection( *self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw )
            return conn
        return self.do_open( build, req )

class Result:
    """ object store for HTTP responses """
    def __init__( self, host, port, working ):
        self.state = {
            "host"    : host,
            "port"    : port,
            "working" : working
        }

class Scanner:
    """ manage work queue for proxy tests """
    def __init__( self, proxylist, workers ):
        """ initialize main object and configure state """
        self.state = {
            "proxies" : Queue(),
            "results" : Queue(),
            "tester"  : "https://blackcatz.org/ip",
            "procs"   : [],
            "workers" : workers
        }

        for worker in range( 0, int( self.state["workers"] ) + 1 ):
            """ start worker processes """
            proc = Process( target=self.tester )
            self.state["procs"].append( proc )
            proc.start()

        """ start a single printer process """
        proc = Process( target=self.printer )
        self.state["procs"].append( proc )
        proc.start()

        for proxy in open( proxylist, "r" ).readlines():
            self.state["proxies"].put( proxy.rstrip() )

    def tester( self ):
        """ test a proxy to see if it works """
        while True: #keep checking for work
            if self.state["proxies"].empty() is not True:
                proxy = self.state["proxies"].get()
                host = proxy.split( ":" )[0]
                port = int( proxy.split( ":" )[1]
                try:
                    opener = urllib2.build_opener( SocksiPyHandler( socks.PROXY_TYPE_SOCKS5, host, port ) )
                    if host in opener.open( self.state["tester"] ).read():
                        self.state["results"].put( Result( host, port, True ) )
                    else:
                        self.state["results"].put( Result( host, port, False ) )
                except Exception as E:
                    pass
            else: #wait for queue to be populated
              sleep( 0.2 )
              continue

    def printer( self ):
        """ print test result and status """
        while True: #check for results
            if self.state["results"].empty() is not True:
                result = self.state["results"].get()
                if result.state["working"] is True:
                    print "[+] {}:{} - Working".format( result.state["host"], result.state["port"] )
                else:
                    print "[-] {}:{} - Stale".format( result.state["host"], result.state["port"] )
            else:
                sleep( 0.2 )
                continue

if __name__ == "__main__":
    """ parse switches and start """
    workers   = None
    proxylist = None

    def signal_handler( signal, frame ):
        sys.exit()

    parser = argparse.ArgumentParser( "Multiprocessed socks5 checker" )
    parser.add_argument( "--list"     required=True, help="list of host:port proxies to check" )
    parser.add_argument( "--workers", required=True, help="number of worker processes to use" )

    args = vars( parser.parse_args() )
    
    if args["workers"]:
        workers   = args["workers"]
      
    if args["proxylist"]:
        proxylist = args["proxylist"]
    
    if workers is None:
        workers = 1

    print "[+] Starting ..."
    signal.signal( signal.SIGNINT, signal_handler )
    scanner = Scanner( proxylist, workers )
