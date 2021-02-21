# Name:    Tejas Patel
# UCID"    trp35
# Sectiom: 007
#! /usr/bin/env python3
# Echo Server
import sys
import socket
import datetime, time
import os.path
import codecs

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
dataLen = 1000000

# Create a TCP "welcoming" socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assign IP Address and port number to socket
serverSocket.bind((serverIP, serverPort))
# Listen for incoming connection requests
serverSocket.listen(1)

print('The server is ready to receive on port: ' + str(serverPort) + '\n')

# loop forever listening for incoming connection requests on "welcoming" socket
while True:
    # Accept incoming connection requests; allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()
    print("Socket created for client " + address[0] + ", " + str(address[1]))
    # Receive and print the client data in bytes from "data" socket
    data = connectionSocket.recv(dataLen).decode()
    print("Data from client: " + data)

    s = data.split("\r\n")
    temp = s[0].split("/")
    file = temp[1].split(" ")
    fileNotFound = False
    try:
        f = open(file[0], "r")
        file_contents = ""
        for line in f:
            file_contents += line
        secs = os.path.getmtime(file[0])
        t1 = time.gmtime(secs)
        last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", t1)
    except:
        fileNotFound = True

    t = datetime.datetime.now(datetime.timezone.utc)
    currentTime = t.strftime("%a, %d %b %Y %H:%M:%S GMT")
    if not fileNotFound:
        if ("If-Modified-Since" in data) or ('If-Modified-Since' in str(s[len(s)-3])):
            cache_mod = s[len(s)-3][19:]
            cache_time = time.strptime(cache_mod, "%a, %d %b %Y %H:%M:%S %Z")
            cache_secs = time.mktime(cache_time)
            # print("CACHE MODIFIED12: " + str(cache_secs))
            file_t = time.strptime(last_mod_time, "%a, %d %b %Y %H:%M:%S %Z")
            file_secs = time.mktime(file_t)
            # print("FILE MODIFIED1: " + str(file_secs))
            if cache_secs < file_secs:
                # return as you do when file is not in cache
                content_len = len(file_contents.encode('utf-8'))-1

                dataEcho = "HTTP/1.1 200 OK\r\nDate: " + currentTime + "\r\nLast-Modified: " + last_mod_time + "\r\nContent-Length: " + str(
                    content_len) + "\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n" + file_contents
                connectionSocket.send(dataEcho.encode())
            else:
                # return appropriate not modified response(code 304)
                dataEcho = "HTTP/1.1 304 Not Modified\r\nDate: " + currentTime + "\r\n\r\n"
                connectionSocket.send(dataEcho.encode())

        else:
            content_len = len(file_contents.encode('utf-8'))-1

            dataEcho = "HTTP/1.1 200 OK\r\nDate: " + currentTime + "\r\nLast-Modified: " + last_mod_time + "\r\nContent-Length: " + str(content_len) + "\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n" + file_contents
            connectionSocket.send(dataEcho.encode())
    else:
        dataEcho = "HTTP/1.1 404 Not Found\r\nDate: " + currentTime + "\r\nContent-Length: 0\r\n\r\n"
        connectionSocket.send(dataEcho.encode())
