#! /usr/bin/env python3

import OpenSSL
import ssl
import sys
import socket
import json

if len (sys.argv) !=2 :
    print("Usage: python3 SSLNameExtractor.py [IP Address to test]")
    sys.exit(1)

def getCert(ip):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        s = ctx.wrap_socket(socket.socket())
        s.connect((ip,443))
        cert = s.getpeercert()
        return cert
    except Exception as e:
        print("Oops, something went wrong connecting to the remote system - %s" % e)
        sys.exit(1)

def extractCN(cert):
    try:
        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName']
    except Exception as e:
        issued_to = "Couldn't extract CN - %s" % e
    return issued_to

def extractSAN(cert):
    try:
        san = cert["subjectAltName"]
    except Exception as e:
        san = "Couldn't extract SAN - %s" % e
    return san

def main():
    ip = sys.argv[1]
    print("Grabbing the cert for %s" % ip)
    cert = getCert(ip)
    print("Okay, have the cert. Now extracting the goodies:")
    cn = extractCN(cert)
    san = extractSAN(cert)
    print("\tCN = %s\n\tSAN = %s" % (cn,san))

if __name__ == "__main__":
    main()
