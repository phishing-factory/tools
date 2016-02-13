#!/usr/bin/env python2
#author: mp
#comment: multiprocessed sub domain scanner

from socket import gethostbyname, gaierror
from multiprocessing import Process
from time import sleep
import Queue
import sys
import argparse

class Result:
    """ object store for resolved domains """
    def __init__( self, record, host ):
        """ initialize object data """
        self.record  = record
        self.host    = host

class Scanner:
    
    """ A few functions for managing a queue of requests and
    several worker processes """

    def __init__( self, domain, sublist, workers ): 
        """ initialize main object and configure state """
        self.state = {
            "subs"    : Queue(),
            "results" : Queue(),
            "domain"  : domain,
            "procs"   : [],
            "workers" : workers
        }

        for worker in range( 0, self.state["workers"] + 1 ):
            """ start worker processes """
            proc = Process( target=self.resolver )
            self.state["procs"].append( proc )
            proc.start()

        """ start a single printer process """
        proc = Process( target=self.printer )
        self.state["procs"].append( proc )
        proc.start()

        self.subcount = 0 #number of jobs is number of subs
        for subdomain in open( sublist, "r" ).readlines():
            self.state["subs"].put( subdomain )
            self.subcount += 1

        while True:
            if (( len( self.state["results"] ) + 1 ) == self.subcount ):
                break #workers are probably done

        for proc in self.state["procs"]:
            proc.join() #clean up
            print "[*] Joined on process"

    def resolver( self ):
        """ resolve subdomains in queue """
        while True: #keep checking for work
            sub = self.state["subs"].get_nowait()
            if sub is not None:
                try: #catch if host is not known
                    record = "{}.{}".format( sub, self.state["domain"] )
                    host = gethostbyname( record )
                except giaerror as UNKNOWN:
                    host = None
                self.results.put( Result( record, host ) )
            else: #wait for queue to be populated
                sleep( 0.2 )
                continue

    def printer( self ):
        """ print after resolved """
        while True: #keep checking for results
            result = self.state["results"].get_nowait()
            if result is not None:
                if result.host is not None: #found one :)
                    print "[>] {} : {}",format( result.record, result.host )
            else: #wait for queue to be populated
                sleep( 0.2 )
                continue

if __name__ == "__main__":
    """ parse switches and start """
    workers = None
    domain  = None
    sublist = None

    parser = argparse.ArgumentParser( "Multiprocessed Sub Domain Scanner" )
    parser.add_argument( "--domain",  required=True,  help="domain to scan" )
    parser.add_argument( "--sublist", required=True,  help="list of sub domains" )
    parser.add_argument( "--workers", required=False, help="number of procs to spawn" )
    args = vars( parser.parse_args() )

    if args["workers"]:
        workers = args["workers"]
    
    if args["sublist"] and args["domain"]:
        sublist = args["sublist"]
        domain  = args["domain"]

    if workers is None:
        workers = 1

    print "[+] Starting..."
    scanner = Scanner( domain, sublist, workers )
