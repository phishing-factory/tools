#!/usr/bin/env python2
#author: mp
#comment: multiprocessed directory buster

from multiprocessing import Process, Queue
from time import sleep
import urllib
import argparse 
import sys
import signal

class Result:
    """ object store for HTTP responses """
    def __init__( self, code, size, uri ):
        self.response = { 
            "code" : code,
            "size" : size,
        }
        self.uri = uri

class Scanner:
    
    """ A few functions for managing a queue for web requests
    and several workers """
    
    def __init__( self, url, dirlist, workers ):
        """ initialize main object and configure state """
        self.state = {
            "dirs"    : Queue(),
            "results" : Queue(),
            "url"     : url,
            "procs"   : [],
            "workers" : workers
        }

        for worker in range( 0, int( self.state["workers"] ) + 1 ):
            """ start worker processes """
            proc = Process( target=self.requester )
            self.state["procs"].append( proc )
            proc.start()

        """ start a single printer process """
        proc = Process( target=self.printer )
        self.state["procs"].append( proc )
        proc.start()

        self.dircount = 0 #number of jobs is number of dirs
        for directory in open( dirlist, "r" ).readlines():
            self.state["dirs"].put( directory.rstrip( "\n" ) )
            self.dircount += 1

    def requester( self ):
        """ request resources from web server """
        if self.state["url"].endswith( "/" ):
            self.state["url"] = self.state["url"].rstrip( "/" )
        while True: #keep checking for work
            if self.state["dirs"].empty() is not True:
                directory = self.state["dirs"].get()
                uri = "{}/{}".format( self.state["url"], directory )
                try: #catch request errors
                    #print "[***] Checking {}".format( uri )
                    resp = urllib.urlopen( uri )
                    code = int( resp.getcode() )
                    size = len( resp.read() )
                except Exception as E:
                    code = None
                    size = None
                if code is not None:
                    self.state["results"].put( Result( code, size, uri ) )
            else: #wait for queue to be populated
                sleep( 0.2 )
                continue
    
    def printer( self ):
        """ print after request """
        while True: #keep checking for results
            if self.state["results"].empty() is not True:
                result = self.state["results"].get()
                print "[{}] Size: {} - {}".format( 
                    result.response["code"], 
                    result.response["size"], 
                    result.uri 
                )
            else: #wait for queue to be populated
                sleep( 0.2 )
                continue

if __name__ == "__main__":
    """ parse switches and start """
    workers = None
    url     = None
    dirlist = None

    def signal_handler( signal, frame ):
        sys.exit( 0 )

    parser = argparse.ArgumentParser( "Multiprocessed Directory Scanner" )
    parser.add_argument( "--url",     required=True,  help="url to scan" )
    parser.add_argument( "--workers", required=False, help="number of procs to spawn" )
    parser.add_argument( "--dirlist", required=True,  help="list of directories" )
    args = vars( parser.parse_args() )

    if args["workers"]:
        workers = args["workers"]

    if args["dirlist"] and args["url"]:
        dirlist = args["dirlist"]
        url = args["url"]

    if workers is None:
        workers = 1

    print "[+++] Starting..."
    signal.signal( signal.SIGINT, signal_handler )
    scanner = Scanner( url, dirlist, workers )
