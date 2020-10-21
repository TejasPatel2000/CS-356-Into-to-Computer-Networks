# Name:    Tejas Patel
# UCID"    trp35
# Sectiom: 007
# /usr/bin/env python3
# Echo Client
import sys
import socket
import time
import requests
import struct


# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
# count = int(sys.argv[3])
# Need to make data a struct of 1 and the sequence number
# data = 'X' * count  # Initialize data to be sent

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# https://docs.python.org/3/library/socket.html Used this site to learn how to set socket timeout
clientsocket.settimeout(1)
listRTT = []
seqNum = 1
print("Pinging " + host + ", " + str(port) + ": ")
msg_type = 1
totalRTT = 0
packetsLost = 0
while seqNum <= 10:
    # used the site in line below to understand socket timeouts needed to complete assignment.
    # https://docs.python.org/3/library/socket.html Specifically used the socket.timeout section necessary in the try
    # except used the site in the line below to help with the try except block
    # https://www.kite.com/python/examples/5615/socket-handle-a-socket-timeout
    try:
        # use https://docs.python.org/3/library/struct.html  & https://www.askpython.com/python-modules/python-struct-module
        # to understand how structs work and convert to big Endian
        data = struct.pack('!hh', msg_type, seqNum)
        # Send data to server and start timer.
        # used https://docs.python.org/3/library/time.html to learn about diff functions like time.time() time.sleep()
        # used https://www.geeksforgeeks.org/program-calculate-round-trip-time-rtt/ to better understand RTT
        start_time = time.time()
        clientsocket.sendto(data, (host, port))
        time.sleep(.0001)
        dataEcho, address = clientsocket.recvfrom(1024)
        recvData = struct.unpack('!hh', dataEcho)
        end_time = time.time()
        RTT = end_time-start_time
        listRTT.append(RTT)
        totalRTT += RTT
        print("Ping message number " + str(seqNum) + " RTT: " + str(RTT) + " secs")
    except socket.timeout:
        packetsLost += 1
        print("Ping message number " + str(seqNum) + " timed out")
    seqNum += 1

listRTT.sort()
print("Statistics:")
print("10 packets transmitted, " + str(10-packetsLost) +" received, " + str(packetsLost*10) + "% packet loss")
print("Min/Max/Av RTT = " + str(listRTT[0]) + " / " + str(listRTT[len(listRTT)-1]) + " / " + str(totalRTT/(len(listRTT))) + " secs")
# Close the client socket
clientsocket.close()
