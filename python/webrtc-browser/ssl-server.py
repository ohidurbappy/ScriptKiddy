from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == '/get/':
            self.wfile.write('On /get/')
            return
        self.wfile.write('On root')
        return    

    def do_POST(self):
        pass

httpd = HTTPServer(('localhost', 4443), Handler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="key.pem", 
        certfile='cert.pem', server_side=True)

httpd.serve_forever()