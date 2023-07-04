from http.server import SimpleHTTPRequestHandler, test
import os
import sys
import base64

key = ""

class AuthHandler(SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def __init__(self, *args, **kwargs):
        kwargs["directory"] = "Logs"
        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)
        
    def do_HEAD(self):
        print("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.get('Authorization') == 'Basic '+ key:
            SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get('Authorization'))
            self.wfile.write('not authenticated')
            pass


if __name__ == '__main__':
    if len(sys.argv)<3:
        print("usage SimpleAuthServer.py [port] [username:password]")
        sys.exit()
    key = base64.b64encode(sys.argv[2].encode()).decode()
    test(HandlerClass=AuthHandler, port = 8000, bind = "0.0.0.0")
