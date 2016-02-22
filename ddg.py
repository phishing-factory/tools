#!/usr/bin/env python2
#author: mp
#comment: scrape results from duck duck go

import urllib2
from BeautifulSoup import BeautifulSoup as Soup
import argparse

def get_links( url ):
    opener = urllib2.build_opener()
    opener.addheaders = [( "User-agent", "Mozilla/5.0" )]
    soup = Soup( opener.open( url ).read() )
    for link in soup.findAll( "div", { "class" : "url" } ):
        print " {}".format( link.text.encode( "utf-8" ).strip() )

if __name__ == "__main__":
    
    query = None
    
    parser = argparse.ArgumentParser( "scrape results from Duck Duck Go" )
    parser.add_argument( "-q", "--query", required=True, help="Search string" )

    args = vars( parser.parse_args() )

    if args["query"]:
        query = args["query"]

    url = "https://duckduckgo.com/html/?q={}".format( query )
    print url
    get_links( url )
