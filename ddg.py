#!/usr/bin/env python2
#author: mp
#comment: scrape results from duck duck go

#currently im only wanting the official site results as im hunting router firmware
#so this script prints only 1 result, i will expand on it later

import urllib2
from BeautifulSoup import BeautifulSoup as Soup
import sys

opener = urllib2.build_opener()
opener.addheaders = [( "User-agent", "Mozilla/5.0" )]
soup = Soup( opener.open( "https://duckduckgo.com/?q={}".format( sys.argv[1] ) ).read() )
for span in soup.findAll( "span", { "class" : "result__url__domain" } ):
    print span.text
