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
# Used https://www.w3schools.com/python/python_file_open.asp to understand how files work
f = open("dns-master.txt", "r").readlines()
# General info on dictionaries https://www.w3schools.com/python/python_dictionaries.asp
fileDict = {}
# Used https://www.w3schools.com/python/python_file_open.asp to understand how iterate over lines in a file
for x in f:
    if x[0:4] == "host":
        # Split string into hostname and the total time and ip address
        s1 = x.split(' A IN ')
        # add that to the dictionary so its easy to search for
        fileDict[s1[0]] = s1[1]

msg_type = 2
# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)
    # Unpack data to get all necessary information and find answer
    var = struct.unpack('!hhihh', data[0:12])
    q = struct.unpack('!hhihh' + str(var[3]) + 's', data)
    question=str(q[5].decode())
    # Alter string so its only hostname
    question = question[0:(len(question)-5)]
    message_id = q[2]
    questionLength = q[3]
    #If the hostname in question exists then get answer and send back to client, else just send back to client without answer
    if question in fileDict:
        return_code = 0
        answer = question + " A IN " + fileDict[question]
        answerLength = len(answer)-1
        sendBack = struct.pack('!hhihh'+ str(questionLength) + 's' + str(answerLength) + 's', msg_type, return_code, message_id, questionLength, answerLength, q[5], answer.encode())
    else:
        return_code = 1
        answerLength = 0
        sendBack = struct.pack('!hhihh' + str(questionLength) + 's', msg_type, return_code, message_id, questionLength, answerLength, q[5])

    # Echo back to client
    serverSocket.sendto(sendBack, address)

