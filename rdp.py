#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2029 Zhiming Huang
#
import select
import socket
import sys
import queue
import time
import re
import os

# Create a TCP/IP socket
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverPort = int(sys.argv[2])
ip_addy = sys.argv[1]
# Bind the socket to the port
server_address = ('', serverPort)
#print('starting up on {} port {}'.format(*server_address),
#      file=sys.stderr)
udp_sock.bind(server_address)

# input & output files
readfile = sys.argv[3]
outputfile = sys.argv[4]

# OUTPUT FORMAT: DATE: EVENT; COMMAND; Sequence|ACK: value; Length|Window: Value


# Sockets from which we expect to read
inputs = [udp_sock]

# Sockets to which we expect to write
outputs = [udp_sock]

# Outgoing message queues (socket:Queue)
message_queues = {}


# request message
request_message = {}

requestLine = []

timeout = 30

lastmessage = 'not empty'

# recieve buffer
rcv_buf = []

# send buffer
snd_buf = []

synFormat = "SYN\nSequence: 99\nLength: 0\n\n"
synResp = "ACK\nWindow: 1024\nAcknowlegment: 100\n\n"

datFormat = "DAT\nSequence: 100\nLength: 100\n\n/.*"
datResp = "ACK\nWindow: 924\nAcknowlegment: 200\n\n"

while inputs:

    # Wait for at least one of the sockets to be
    # ready for processing
#    print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,
                                                    outputs,
                                                    inputs,
                                                    timeout)

    # Handle inputs


    for udpSocket in readable:

        # recieve data and append to rcv_buf
        print(udpSocket)

        # if message cannot be recognized:
            
                # write rst packet into snd_buf




    # Handle outputs
    for udpSocket in writable:
        bytes_sent = udp_sock.send(snd_buf)
        # remove the bytes already sent from the snd_buf

                    
                

    # Handle "exceptional conditions"
    for s in exceptional:
        #print('exception condition on', s.getpeername(),
         #     file=sys.stderr)
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
    
    # if s not in readable and writable and exceptional:
    #      #handle timeout events
    #      socket.settimeout(30)
