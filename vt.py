#!/usr/bin/env python2
#author: mp
#comment: using VT API, check an IPv4 address for nasty findings

import urllib
import re
import sys
import json

class VirusTotal:
    """ initalize and define checks """
    def __init__( self, ip ):
        """ set initial state vars """
        self.state = {
            "url"  : "https://www.virustotal.com/vtapi/v2/ip-address/report",
            "ip"   : None,
            "key"  : "__INSERT_API_KEY_HERE__",
            "resp" : None
        }
        
        """ match on regex and update state with json response """
        if re.match( r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip ):
            self.state["ip"] = ip
            self.state["resp"] = urllib.urlopen( "{}?{}".format( self.state["url"], urllib.urlencode( { 
                "ip"     : self.state["ip"],
                "apikey" : self.state["key"]
            })))
            self.state["resp"] = json.loads( self.state["resp"].read() )

    def check_known_samples( self ):
        try: #check for known samples
            print "[+] Checking {} for known samples".format( self.state["ip"] )
            count = 0
            if self.state["resp"]["detected_downloaded_samples"]:
                print "[!] Malicous samples detected!!"
                for finding in self.state["resp"]["detected_downloaded_samples"]:
                    count += 1
                    if count <= 10:
                        print "[>] {} {}/{} {}".format( 
                            finding["date"],
                            finding["positives"],
                            finding["total"],
                            finding["sha256"]
                        )
                if count > 0:
                    print "[^] Virus Total detected {} known samples for {}".format( 
                        str( count ), self.state["ip"] 
                    )
            if count == 0:
                print "[-] Virus Total detected 0 known samples on {}".format( 
                    self.state["ip"] 
                )
        except:
            pass

    def check_unknown_samples( self ):
        try: #check for unknown samples
            print "[+] Checking {} for unknown samples".format( self.state["ip"] )
            count = 0
            if self.state["resp"]["undetected_downloaded_samples"]:
                print "[!] Unknown samples detected!!"
                for finding in self.state["resp"]["undetected_downloaded_samples"]:
                    count += 1
                    if count <= 10:
                        print "[>] {} {}/{} {}".format(
                            finding["date"],
                            finding["positives"],
                            finding["total"],
                            finding["sha256"]
                        )
                if count > 0:
                    print "[^] Virus Total detected {} unknown samples for {}".format(
                        str( count ), self.state["ip"]
                    )
            if count == 0:
                print "[-] Virus Total detected 0 unknown samples on {}".format(
                    self.state["ip"]
                )
        except:
            pass

    def check_suspicious_urls( self ):
        try: #check for urls hosted on target ip
            print "[+] Checking {} for suspicious URLz".format( self.state["ip"] )
            count = 0
            if self.state["resp"]["detected_urls"]:
                print "[!] Suspicious URLz identified!!"
                for finding in self.state["resp"]["detected_urls"]:
                    count += 1
                    if count <= 10:
                        print "[>] {} {}/{} {}".format(
                            finding["scan_date"],
                            finding["positives"],
                            finding["total"],
                            finding["url"]
                        )
                if count > 0:
                    print "[^] Virus Total detected {} suspicious URLz for {}".format(
                        str( count ),
                        self.state["ip"]
                    )
            if count == 0:
                print "[-] Virus Total discovered 0 suspicious URLz associated with {}".format(
                    self.state["ip"]
                )
        except Exception as E:
            print E

def usage():
    print "./vt.py <ipv4 address>"
    sys.exit()

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
    except:
        usage()

    vt = VirusTotal( ip )
    if vt.state["ip"] is not None:
        vt.check_known_samples()
        vt.check_unknown_samples()
        vt.check_suspicious_urls()
    else:
        usage()
