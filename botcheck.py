#!/usr/bin/env python2
#author: mp
#comment: scrape abuse.ch zeus|palevo|feodo trackers for an IPv4 address
# spyeye has been discontinued so not included in this scraper

from BeautifulSoup import BeautifulSoup as Soup
import urllib2
import argparse
import sys
import re

class Botcheck:
    """ check abuse.ch trackers for an IPv4 address """
    def __init__( self, ipv4 ):
        """ check if ipv4 is valid and build request opener """
        if re.match( r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ipv4 ):
            self.opener = urllib2.build_opener()
            self.opener.addheaders = [( "User-agent", "Mozilla/5.0" )]
            self.ipv4 = ipv4
        else:
            print "Thats not a valid IPv4 address"
            sys.exit()

    def zeus( self ):
        """ check IPv4 for zeus C&C """        
        try: #catch request if error
            url  = "https://zeustracker.abuse.ch/monitor.php?search={}".format( self.ipv4 )
            data = Soup( self.opener.open( url ).read() )
            for div in data.findAll( "div", { "class" : "ContentBox" } ):
                for line in div.findAll( [ "h2", "p", "tr" ] ):
                    if "You can search" not in line:
                        if line.findAll( "td" ):
                            cols = line.findAll( "td" )
                            cols = [ ele.text.strip() for ele in cols ]
                            print " ".join( [ ele.encode( "ascii" ) for ele in cols if ele ] )
                        else:
                            line = line.text
                            if "You can search" not in line:
                                print line
        except Exception as E:
            print "Error: {}".format( E )
            pass
        
    def palevo( self ):
        """ check IPv4 for palevo C&C """
        try: #catch request if error
            url  = "https://palevotracker.abuse.ch/?ipaddress={}".format( self.ipv4 )
            data = Soup( self.opener.open( url ).read() )
            for div in data.findAll( "div", { "class" : "ContentBox" } ):
                for line in div.findAll( [ "h2", "h3", "p", "tr" ] ):
                    if line.findAll( "td" ):
                        cols = line.findAll( "td" )
                        cols = [ ele.text.strip() for ele in cols ]
                        print " ".join( [ ele.encode( "ascii" ) for ele in cols if ele ] )
                    else:
                        line = line.text
                        print line
        except Exception as E:
            print "Error: {}".format( E )
            pass

    def feodo( self ):
        """ check IPv4 for feodo C&C """
        try: #catch request if error
            url  = "https://feodotracker.abuse.ch/host/{}/".format( self.ipv4 )
            data = Soup( self.opener.open( url ).read() )
            for div in data.findAll( "div", { "class" : "MainContainer" } ):
                for line in div.findAll( [ "h1", "h2", "p", "td" ] ):
                    if line.findAll( "td" ):
                        cols = line.findAll( "td" )
                        cols = [ ele.text.strip() for ele in cols ]
                        print " ".join( [ ele.encode( "ascii" ) for ele in cols if ele ] )
                    else:
                        line = line.text
                        print line
        except Exception as E:
            print "Error: {}".format( E )
            pass

    def check_all( self ):
        self.zeus()
        self.palevo()
        self.feodo()

if __name__ == "__main__":

    ipv4     = None
    rancheck = False
    parser = argparse.ArgumentParser( "check abuse.ch trackers for an IPv4 address" )
    parser.add_argument( "--ip",     required=True,  help="IPv4 address to check for" )
    parser.add_argument( "--zeus",   required=False, help="Check for Zeus C&C",   action="store_true" )
    parser.add_argument( "--palevo", required=False, help="Check for palevo C&C", action="store_true" )
    parser.add_argument( "--feodo",  required=False, help="Check for Feodo C&C",  action="store_true" )
    parser.add_argument( "--all",    required=False, help="Perform all checks",   action="store_true" )

    args = vars( parser.parse_args() )

    if args["ip"]:
        ipv4 = args["ip"]
        botcheck = Botcheck( ipv4 )
    if args["all"]:
        botcheck.check_all()
        rancheck = True
    if args["zeus"]:
        botcheck.zeus()
        rancheck = True
    if args["palevo"]:
        botcheck.palevo()
        rancheck = True
    if args["feodo"]:
        botcheck.feodo()
        rancheck = True
    if rancheck is False:
        print "You didnt specify a check"
        sys.exit()
