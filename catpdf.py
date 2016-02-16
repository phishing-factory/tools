#!/usr/bin/env python2
#author: mp
#comment: a tiny script to convert a pdf doc to text so that you can grep for keywords

import pyPdf
import sys

try:
    pdf = pyPdf.PdfFileReader( open( sys.argv[1], "r" ) )
    for page in pdf.pages:
        print page.extractText()
except:
  print "Usage: {} <pdf>".format( sys.argv[0] )
