# Name:    Tejas Patel
# UCID"    trp35
# Sectiom: 007
#! /usr/bin/env python3
# Echo Server
import sys
import socket
import random
import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")
# loop forever listening for incoming UDP messages
msg_type = 2
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)
    var = struct.unpack('!hh', data)
    # Call random number here after you received data from client to decide whether or not to send data back or not
    # used https://docs.python.org/3/library/random.html
    rand_num = random.randint(0, 10)

    if rand_num < 4:
        print("Message with sequence number " + str(var[1]) + " dropped")
    else:
        # Echo back to client
        sendBack = struct.pack('!hh', msg_type, var[1])
        print("Responding to ping request with sequence number " + str(var[1]))
        serverSocket.sendto(sendBack, address)

