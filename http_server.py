from threading import Thread
import http.server
import socketserver

PORT = 7000
IP = "192.168.56.101"

Handler = http.server.SimpleHTTPRequestHandler


def start_http_server():
    socketserver.TCPServer((IP, PORT), Handler).serve_forever()
    print("HTTP server serving at port", PORT, "and IP", IP)


server_thread = Thread(target=start_http_server, name='http_server_thread', daemon=True)
