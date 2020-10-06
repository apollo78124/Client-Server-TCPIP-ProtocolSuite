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
import pathlib
tcpserverHost = '192.168.1.75'        # Default IP to connect to
tcpBind=''
tcpserverPort = 7005               # Default port number
udpPort = 7006
udpIP = ""
udpBind = ""
buffer = 1024

commandLineActive = True
connectionSetup = True

messages = []  # Default text (ASCII) message
                                # requires bytes: b'' to convert to byte literal

#tcpsockobj = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
#tcpsockobj.connect((tcpserverHost, tcpserverPort))   # connect to server IP + port

tcpserverHost = input("### Connection Init ### \nServer Address to Connect to: ")

while commandLineActive:
    messages = []
    userCommand = input("command to server: ")
    tcpsockobj = socket(AF_INET, SOCK_STREAM)
    tcpsockobj.connect((tcpserverHost, tcpserverPort))
    if userCommand == "quit":
        tcpsockobj.close()
        commandLineActive = False
        break
    messages.append(bytes(userCommand, 'ascii'))

    for line in messages:
        tcpsockobj.send(line)                      # send user message
        data = tcpsockobj.recv(1024)               # read server response
        print('Message from the Server:', data)
    if userCommand == "GET":
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        udpSocket.bind((udpBind, udpPort))

        print('Waiting For First UDP Data...')
        udpData, udpAddr = udpSocket.recvfrom(1024)
        if udpData:
            print("File name:", udpData)
            file_name = udpData.strip()
            f = open(file_name, 'wb')
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
        tcpsockobj.close()
    if userCommand == "SEND":
        udpIP = tcpserverHost
        fileToSend = input("Type the name of the file you want to send \n >>>  ")
        file = pathlib.Path(fileToSend)
        if file.exists():
            print("File exists. Preparing the file to send...")
            tcpsockobj.send(b'Exists')
            udpSocketObject = socket(AF_INET, SOCK_DGRAM)
            udpSocketObject.sendto(bytes(fileToSend, 'ascii'), (udpIP, udpPort))
            print("UDP Connection opened port number: ", udpPort)

            print("Waiting for server file creation confirmation...")
            tcpData = tcpsockobj.recv(1024)
            print("File Creation Confirmed")

            print("Sending %s ..." % fileToSend)
            file = open(fileToSend, "r")
            data = file.read(buffer)

            while data:
                if udpSocketObject.sendto(data.encode('utf-8'), (udpIP, udpPort)):
                    data = file.read(buffer)
                    time.sleep(0.02)  # Give receiver a bit time to save
            print("file send complete")
            udpSocketObject.close()
            file.close()
            continue
        else:
            print("File does not exist, exiting SEND command")
            tcpsockobj.send(b'NotExisting')
            tcpsockobj.close()
