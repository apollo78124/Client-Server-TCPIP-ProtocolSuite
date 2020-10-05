#!/usr/bin/python

"""
Basic TCP echo server. Listen for a client conenction, reads the message
and then echoes the message back to the client.

"""

from socket import *
tcpHost = ''                                 # '' to set the default IP to localhost
tcpPort = 7005                               # Default port number
udpPort = 7006
udpSocketObject = socket(AF_INET, SOCK_DGRAM)

tcpSocketObject = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
tcpSocketObject.bind((tcpHost, tcpPort))              # bind it to server port number
tcpSocketObject.listen(5)

while True:                                 # listen until process killed
    tcpConnection, tcpAddress = tcpSocketObject.accept()
    print('Client Connection:', tcpAddress)    # Print the connected client address
    while True:
        tcpData = tcpConnection.recv(1024)        # read the client message
        if not tcpData: break
        if tcpData == b'GET':
            tcpConnection.send(b'GET Command sent')
            print('Client Says: ', tcpData)
            break
#        udpSocketObject = socket(AF_INET, SOCK_DGRAM)
#        udpSocketObject.bind(("", udpPort))
        tcpConnection.send(b'Echo => ' + tcpData)   # Echo it back send data using "b" to format string as byte literal (ASCII)
        print('Client Says: ', tcpData)
#    tcpConnection.close()
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
