#! /usr/bin/env python3
# Echo Server
import sys
import socket

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(100)
    print("Receive data from client " + address[0] + ", " + str(address[1]) + ": " + data.decode())

    # Echo back to client
    print("Sending data to   client " + address[0] + ", " + str(address[1]) + ": " + data.decode())
    serverSocket.sendto(data, address)

