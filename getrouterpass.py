#!/usr/bin/env python2
#author:mp
#comment: scrape findings from http://www.routerpasswords.com/
# for sys.argv[1]

import sys
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup as Soup

opener  = urllib2.build_opener()
opener.addheader = [( "User-agent", "Mozilla/5.0" )]
url     = "http://www.routerpasswords.com/"
data    = {
    "findpass"     : "1",
    "router"       : sys.argv[1],
    "findpassword" : "Find+Password"
}
request = opener.open( url, data=urllib.urlencode( data ) ).read()
soup    = Soup( request )
for table in soup.findAll( "tr" ):
    cols = table.findAll( "td" )
    cols = [ ele.text.strip() for ele in cols ]
    print " ".join( [ ele.encode( "ascii" ) for ele in cols if ele ] )
