#!/usr/bin/env python2
#simple link spider

import urllib2
from BeautifulSoup import BeautifulSoup as Soup
import sys
import re

target = sys.argv[1]
domain = target.split( "://" )[1]
links = []

if re.match( r"^http", target ):
    proto = "http"
elif re.match( r"^https", target ):
    proto = "https"

def parse( url ):

    opener = urllib2.build_opener()
    opener.addheader = [( "User-agent", "Mozilla/5.0" )]
    soup = Soup( opener.open( sys.argv[1] ).read() )

    for i in soup.findAll( "a" ):
        link = i['href']
        if "http://" in link:
            url = link
            links.append( url )
        elif link.startswith( "//".format( domain ) ):
            if domain in link:
                url = "{}://{}".format( proto, link.replace( "//", "" ) )
                links.append( url )
        else:
            url = "{}{}".format( target, link )
            links.append( url )

parse( target )
with open( "crawl.log", "a" ) as log:
    for i in links:
        print i
        log.write( "{}\n".format( i ) )
        parse( i )
        links.remove( i )
