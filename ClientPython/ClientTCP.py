#!/usr/bin/python

"""
Basic TCP echo client. Sends a default message string to data to the server,
and print server's echo. User can also specify an IP and message string to
sent to the server.

NOTE: Specify commnadline arguments as follows:

./echo-client.py [host]
or
./echo-client.py [host] [message]

"""

import sys
import time
from socket import *
import select
tcpserverHost = 'localhost'        # Default IP to connect to
tcpserverPort = 7005               # Default port number
udpPort = 7006
udpHost = "localhost"

commandLineActive = True

messages = []  # Default text (ASCII) message
                                # requires bytes: b'' to convert to byte literal
if len(sys.argv) == 2:
    tcpserverHost = sys.argv[1]    # User has provided a server IP at cmd line arg 1
    if len(sys.argv) > 2:       # User-defined message from cmd line args 2
        messages = (x.encode() for x in sys.argv[2:])

tcpsockobj = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
tcpsockobj.connect((tcpserverHost, tcpserverPort))   # connect to server IP + port
while commandLineActive:
    messages = []
    userCommand = input("command: ")
    if userCommand == "quit":
        tcpsockobj.close()
        commandLineActive = False
        break;
    messages.append(bytes(userCommand, 'ascii'))

    for line in messages:
        tcpsockobj.send(line)                      # send user message
        data = tcpsockobj.recv(1024)               # read server response
        print('Message from the Server:', data)
    if userCommand == "GET":
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        udpSocket.bind((udpHost, udpPort))
        udpData, udpAddr = udpSocket.recvfrom(1024)
        if udpData:
            print("File name:", udpData)
            file_name = udpData.strip()
            f = open(file_name, 'wb')
            time.sleep(3)
            tcpsockobj.send(bytes("File Created", 'ascii'))
            while True:
                ready = select.select([udpSocket], [], [], 3)
                if ready[0]:
                    udpData, udpAddr = udpSocket.recvfrom(1024)
                    f.write(udpData)
                else:
                    print("%s Finish!" % file_name)
                    f.close()
                    break
        udpSocket.close()

