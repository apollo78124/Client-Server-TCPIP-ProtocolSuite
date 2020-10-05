#!/usr/bin/python

from socket import *

udpPort = 7006
udpHost = "localhost"
udpSockobj = socket(AF_INET, SOCK_DGRAM)
udpSockobj.bind(("", 0))
udpSockobj.sendto(bytes("We have Ingition!", 'ascii'), (udpHost, udpPort))