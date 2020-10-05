#!/usr/bin/python

"""
Basic TCP echo server. Listen for a client conenction, reads the message
and then echoes the message back to the client.

"""
import time
from socket import *
tcpIP = ''                                 # '' to set the default IP to localhost
tcpPort = 7005                               # Default port number
udpIP = '127.0.0.1'
udpPort = 7006
buffer = 1024

tcpSocketObject = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
tcpSocketObject.bind((tcpIP, tcpPort))              # bind it to server port number
tcpSocketObject.listen(5)

while True:                                 # listen until process killed
    tcpConnection, tcpAddress = tcpSocketObject.accept()
    print('Client Connection:', tcpAddress)    # Print the connected client address
    while True:
        tcpData = tcpConnection.recv(1024)        # read the client message
        if not tcpData: break
        if tcpData == b'GET':
            tcpConnection.send(b'GET Command sent, file is to be sent shortly')
            file_name = "TestFile1.txt"
            print('Client Says: ', tcpData)
            udpSocketObject = socket(AF_INET, SOCK_DGRAM)
            udpSocketObject.sendto(bytes(file_name, 'ascii'), (udpIP, udpPort))
#           udpSocketObject.bind((udpIP, udpPort))
            print("UDP Port: ", udpPort)
            print ("Sending %s ..." % file_name)

            file = open(file_name, "r")
            data = file.read(buffer)
            while data:
                if udpSocketObject.sendto(data.encode('utf-8'), (udpIP, udpPort)):
                    data = file.read(buffer)
                    time.sleep(0.02)  # Give receiver a bit time to save
            print("file send complete")
            udpSocketObject.close()
            file.close()
            break
#        udpSocketObject = socket(AF_INET, SOCK_DGRAM)
#        udpSocketObject.bind(("", udpPort))
        tcpConnection.send(b'Echo => ' + tcpData)   # Echo it back send data using "b" to format string as byte literal (ASCII)
        print('Client Says: ', tcpData)
    tcpConnection.close()
#!/usr/bin/python

# from socket import *
#
# udpPort = 7006
# udpSocketObject = socket(AF_INET, SOCK_DGRAM)
# udpSocketObject.bind(("", udpPort))
# print ("waiting on port:", udpPort)
# while 1:
#     udpData, udpAddr = udpSocketObject.recvfrom(1024)
#     print ("Received: ", udpData, "From: ", udpAddr)
