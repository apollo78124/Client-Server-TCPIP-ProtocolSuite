#!/usr/bin/python

"""
Basic TCP echo server. Listen for a client conenction, reads the message
and then echoes the message back to the client.

"""
import time
import select
from socket import *
tcpIP = '192.168.1.75'                                      # '' to set the default IP to localhost
tcpPort = 7005                               # Default port number
udpIP = 'localhost'
udpPort = 7006
buffer = 1024
tcpIP = input("$$$Server init$$$\nType bind server address >>> ")
udpIP = tcpIP
tcpSocketObject = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
tcpSocketObject.bind((tcpIP, tcpPort))              # bind it to server port number
tcpSocketObject.listen(5)
print('Listening...')
while True:                                 # listen until process killed
    tcpConnection, tcpAddress = tcpSocketObject.accept()
    print('Client Connection:', tcpAddress)    # Print the connected client address
    while True:
        tcpCommandFromClient = tcpConnection.recv(1024)        # read the client message
        if not tcpCommandFromClient: break

        if tcpCommandFromClient == b'GET':
            tcpConnection.send(b'GET Command sent, file is to be sent shortly')
            file_name = "TestFile1.txt"
            print('Client Says: ', tcpCommandFromClient)
            udpSocketObject = socket(AF_INET, SOCK_DGRAM)
#            udpSocketObject.bind((udpIP, udpPort))
            udpIP = tcpAddress[0]
            udpSocketObject.sendto(bytes(file_name, 'ascii'), (udpIP, udpPort))

            print("Waiting for client confirmation...")
            tcpData = tcpConnection.recv(1024)
            print("UDP Port: ", udpPort)
            print("File Creation Confirmed")
            print("Sending %s ..." % file_name)
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
        if tcpCommandFromClient == b'SEND':
            udpSocket = socket(AF_INET, SOCK_DGRAM)
            udpSocket.bind((udpIP, udpPort))
            tcpConnection.send(b'SEND Command sent')
            tcpData = tcpConnection.recv(1024)
            if tcpData == b'NotExisting':
                break
            udpData, udpAddr = udpSocket.recvfrom(1024)
            if udpData:
                print("File name:", udpData)
                file_name = udpData.strip()
                f = open(file_name, 'wb')
                tcpConnection.send(bytes("File Created", 'ascii'))
                while True:
                    ready = select.select([udpSocket], [], [], 3)
                    if ready[0]:
                        udpData, udpAddr = udpSocket.recvfrom(1024)
                        f.write(udpData)
                    else:
                        print("%s File Import Finish!" % file_name)
                        udpSocket.close()
                        f.close()
                        break
        else :
            tcpConnection.send(b'Echo => ' + tcpCommandFromClient)   # Echo it back send data using "b" to format string as byte literal (ASCII)
            print('Client Said: ', tcpCommandFromClient)
 #           udpData, udpAddr = udpSocket.recvfrom(1024)    #Receive filename from the client.

#       udpSocketObject = socket(AF_INET, SOCK_DGRAM)
#       udpSocketObject.bind(("", udpPort))

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
