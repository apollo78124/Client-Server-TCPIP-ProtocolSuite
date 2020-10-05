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
from socket import *
tcpserverHost = 'localhost'        # Default IP to connect to
tcpserverPort = 7005               # Default port number

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
        break;
    messages.append(bytes(userCommand, 'ascii'))

    for line in messages:
        tcpsockobj.send(line)                      # send user message
        data = tcpsockobj.recv(1024)               # read server response
        print('Received From Server:', data)
