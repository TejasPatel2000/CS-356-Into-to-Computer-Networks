# Name:    Tejas Patel
# UCID:    trp35
# Section: 007
# /usr/bin/env python3
# Client
import sys
import socket
import struct
import datetime, time
import os.path

# Get the server hostname, port and hostname as command line arguments
url = str(sys.argv[1])

# Create TCP client socket. Note use of SOCK_STREAM for TCP packet
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# https://docs.python.org/3/library/socket.html Used this site to learn how to set socket timeout
#clientsocket.settimeout(1)
# Initialize variables
trySend = 1
s = url.split("/")
filename = s[1]
s = url.split(":")
temp = s[1].split("/")
host = s[0]
port = temp[0]
cacheBool = False

temp_file = filename.split(".")
cache_file = "cache-" + str(temp_file[0])+".txt"

try:
    f = open(cache_file)
    f.close()
    cacheBool = True
except:
    cacheBool = False
# Create TCP connection server
#print("Connecting to : " + host + ", " + str(port))
clientsocket.connect((host, int(port)))

if not cacheBool:
    data = "GET /" + str(filename) + " HTTP/1.1\r\n" + "Host: " + str(host) + ":" + str(port) + "\r\n\r\n"
    # Send encoded data through TCP connection
    print(str(data))
    clientsocket.send(data.encode())

    # Receive the server response
    dataEcho = clientsocket.recv(1024)
    # Display the decoded server response as an output
    if "404" not in dataEcho.decode():
        f = open(cache_file, "w")
        returnedData = dataEcho.decode()
        print(returnedData)
        s = returnedData.split("\r\n")
        f.write(str(s[len(s)-1]))
    else:
        t = datetime.datetime.now(datetime.timezone.utc)
        currentTime = t.strftime("%a, %d %b %Y %H:%M:%S %Z")
        print(dataEcho.decode())
       # print("HTTP/1.1 404 Not Found\r\nDate: " + currentTime + "\r\nContent-Length: 0\r\n\r\n")

else:
    secs = os.path.getmtime(cache_file)
    t1 = time.gmtime(secs)
    last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", t1)
    data = "GET /" + str(filename) + " HTTP/1.1\r\n" + "Host: " + str(host) + ":" + str(port) + "\r\n" + "If-Modified-Since: " + last_mod_time +  "\r\n\r\n"

    # Send encoded data through TCP connection
    print(str(data))
    clientsocket.send(data.encode())

    # Receive the server response
    dataEcho = clientsocket.recv(1000000)
    # Display the decoded server response as an output
    if "404" not in dataEcho.decode():
        print(dataEcho.decode())
        returnedData = dataEcho.decode()
        # Here Check if file was modified or not
        if "304" not in returnedData:
            f = open(cache_file, "w")
            s = returnedData.split("\r\n")
            f.write(str(s[len(s) - 1]))
    else:
        t = datetime.datetime.now(datetime.timezone.utc)
        currentTime = t.strftime("%a, %d %b %Y %H:%M:%S %Z")
        print(dataEcho.decode())
        #print("HTTP/1.1 404 Not Found\r\nDate: " + currentTime + "\r\nContent-Length: 0\r\n\r\n")

# Close the client socket
clientsocket.close()
