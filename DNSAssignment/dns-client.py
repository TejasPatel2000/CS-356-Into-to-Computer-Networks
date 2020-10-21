# Name:    Tejas Patel
# UCID"    trp35
# Sectiom: 007
# /usr/bin/env python3
# Echo Client
import sys
import socket
import struct
import random

# Get the server hostname, port and hostname as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostname = str(sys.argv[3])

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# https://docs.python.org/3/library/socket.html Used this site to learn how to set socket timeout
clientsocket.settimeout(1)
# Initialize variables
trySend = 1
msg_type = 1
return_code = 0
message_id = random.randint(0, 100)
question = str(hostname) + " A IN"
questionLength = len(question)
answerLength = 0
# Send initial message info
print("Sending Request to " + str(host) + ", " + str(port))
print("Message ID: " + str(message_id))
print("Question Length: " + str(questionLength) + " bytes")
print("Answer Length: 0 bytes")
print("Question: " + question)
print("\n")
while trySend <= 3:
    # used the site in line below to understand socket timeouts needed to complete assignment.
    # https://docs.pyth8on.org/3/library/socket.html Specifically used the socket.timeout section necessary in the try
    # except used the site in the line below to help with the try except block
    # https://www.kite.com/python/examples/5615/socket-handle-a-socket-timeout
    try:
        # use https://docs.python.org/3/library/struct.html  & https://www.askpython.com/python-modules/python-struct-module
        # to understand how structs work and convert to big Endian
        #Need to encode question string so you can put it in struct pack https://www.programiz.com/python-programming/methods/string/encode
        questionEncoded = question.encode()
        s2 = 's' * len(questionEncoded)
        data = struct.pack('!hhihh' + str(questionLength) + 's', msg_type, return_code, message_id, questionLength, answerLength, questionEncoded)
        # Send Data to Server
        clientsocket.sendto(data, (host, port))
        # Receive Data From Server
        dataEcho, address = clientsocket.recvfrom(1024)
        break
    except socket.timeout:
        # Used if statement to match output as shown in example
        if trySend == 3:
            print("Request timed out... Exiting Program")
        else:
            print("Request timed out...")
            print("Sending Request to " + str(host) + ", " + str(port))
    trySend += 1
# Only output once so it doesn't output each time for timeout case
if trySend <=3 :
    # Unpack data received from server But only first 12 bytes b/c we don't know answer length yet
    recvData = struct.unpack('!hhihh', dataEcho[0:12])
    # Unpack further to get all required info
    q = struct.unpack('!hhihh' + str(recvData[3]) + 's' + str(recvData[4]) + 's', dataEcho)
    # Output information
    print("Received Response from " + str(host) + ", " + str(port))
    print("Return Code: " + str(q[1]))
    print("Message ID: " + str(message_id))
    print("Question Length: " + str(questionLength) + " bytes")
    print("Answer Length: " + str(q[4]) + " bytes")
    print("Question: " + question)
    if q[6].decode() != '':
        print("Answer: " + str(q[6].decode()))


# Close the client socket
clientsocket.close()
