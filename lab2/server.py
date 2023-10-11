#server
from http.server import  HTTPServer, CGIHTTPRequestHandler
adderss = ("localhost", 9999)

server = HTTPServer(adderss, CGIHTTPRequestHandler)
server.serve_forever()