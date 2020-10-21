# Name:    Tejas Patel
# UCID"    trp35
# Sectiom: 007
# /usr/bin/env python3
# Echo Client
import sys
import socket
# import time

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
count = int(sys.argv[3])
data = 'X' * count  # Initialize data to be sent

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# https://docs.python.org/3/library/socket.html Used this site to learn how to set socket timeout
clientsocket.settimeout(1)

checkConn= 0
while checkConn<3:
    # used the site in line below to understand socket timeouts needed to complete assignment.
    # https://docs.python.org/3/library/socket.html Specifically used the socket.timeout section necessary in the try except
    # used the site in the line below to help with the try except block
    # https://www.kite.com/python/examples/5615/socket-handle-a-socket-timeout
    try:
        # Send data to server
        print("Sending data to   " + host + ", " + str(port) + ": " + data)
        clientsocket.sendto(data.encode(), (host, port))
        dataEcho, address = clientsocket.recvfrom(count)
        # Receive the server response
        print("Receive data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())
        break
    except socket.timeout:
        print("Message Timed Out")
        checkConn += 1


# Close the client socket
clientsocket.close()
