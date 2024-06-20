import socket
import threading
import ssl
import dns.resolver
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Server hostname
SERVER_HOSTNAME = 'your_server_hostname'

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

while True:
    try:
        # Accept an incoming connection
        client_socket, address = server_socket.accept()
        logging.info("Connected by %s", address)

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
    except socket.error as e:
        logging.error("Failed to accept incoming connection: %s", e)

def handle_client(client_socket):
    try:
        while True:
            # Receive a message from the client
            message = client_socket.recv(1024)
            logging.info("Received message: %s", message.decode())

            # Send a response back to the client
            response = input("Enter your response: ")
            client_socket.send(response.encode())
    except socket.error as e:
        logging.error("Failed to receive message from client: %s", e)
    finally:
        client_socket.close()

try:
    # Close the server socket
    server_socket.close()
except socket.error as e:
    logging.error("Failed to close server socket: %s", e)
