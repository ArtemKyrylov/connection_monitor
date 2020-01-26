import http.server
import socketserver
import os

PORT = 7000
IP = "127.0.0.1"
Handler = http.server.SimpleHTTPRequestHandler
os.chdir("http_monitor")


def start_http_server():
    with socketserver.TCPServer((IP, PORT), Handler) as httpd:
        print("HTTP server serving at port", PORT, "and IP", IP)
        httpd.serve_forever()


start_http_server()
