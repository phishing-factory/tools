#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup as Soup
import ssl
import urllib2
import sys

version = []
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib2.build_opener()
opener.addheader = [( "User-Agent", "Mozilla/5.0" )]

try:
    soup = Soup( opener.open( "{}/docs/html/index.html".format( sys.argv[1] ) ).read() )
    for div in soup.findAll( "div", { "class" : "related" } ):
        for ul in div.findAll( "ul" ):
            for a in div.findAll( "a" ):
                if "phpMyAdmin" in a.text:
                    version.append( a.text.split( " " )[1] )
except Exception as E:
    print "[!] Error: {}".format( E )
try:
    soup = Soup( opener.open( "{}/Documentation.html".format( sys.argv[1] ) ).read() )
    for div in soup.findAll( "div", { "id" : "header" } ):
        for h1 in div.findAll( "h1" ):
            print h1
except Exception as E:
    print "[!] Error: {}".format( E )

if len( version ) != 0:
    for i in version:
        print "[+] phpMyAdmin version {} detected".format( i )
        break
else:
    print "[!] Failed to enumerate version"
