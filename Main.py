import socket
import threading
import ssl
import dns.resolver
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

# Set up logging
logging.basicConfig(level=logging.INFO)

# Server hostname
SERVER_HOSTNAME = 'https://prepared-tonya-testers001-ac5f43f4.koyeb.app/'

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket with SSL/TLS
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
server_socket = context.wrap_socket(server_socket, server_side=True)

try:
    # Get the server's IP address using reverse DNS lookup
    server_ip = dns.resolver.resolve(SERVER_HOSTNAME, 'A').response[0].address
except dns.resolver.NoAnswer:
    logging.error("Failed to resolve server hostname to IP address")
    exit(1)

try:
    # Bind the socket to the server's IP address
    server_socket.bind((server_ip, 80))
except socket.error as e:
    logging.error("Failed to bind socket to IP address: %s", e)
    exit(1)

# Listen for incoming connections
server_socket.listen(1)

print("Server started. Waiting for connections...")

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

def run_server():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print("Starting httpd...")
    httpd.serve_forever()

try:
    # Run the server
    run_server()
except socket.error as e:
    logging.error("Failed to run server: %s", e)

try:
    # Close the server socket
    server_socket.close()
except socket.error as e:
    logging.error("Failed to close server socket: %s", e)
