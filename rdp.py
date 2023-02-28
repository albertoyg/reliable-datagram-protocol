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

# # sender class
# class rdp_sender:
#     def __init__(self):
#         self.state = 'closed'


def examineArgs():
    if (len(sys.argv) != 5):
        print("error in input")
    else:
        return sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    

def testfile(readfile):
    return os.path.isfile(readfile)


# first check if input is correct
ipaddress, port, readfile, outputfile = examineArgs()

# check if file exists
found = testfile(readfile)

if found == False:
    print("ERROR: file not found")

# Create a TCP/IP socket
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('', port)
#print('starting up on {} port {}'.format(*server_address),
#      file=sys.stderr)
udp_sock.bind(server_address)

# input & output files

# OUTPUT FORMAT: DATE: EVENT; COMMAND; Sequence|ACK: value; Length|Window: Value


# Sockets from which we expect to read
inputs = [udp_sock]

# Sockets to which we expect to write
outputs = [udp_sock]

# Outgoing message queues (socket:Queue)
message_queues = {}


# request message

requestLine = []

timeout = 30

lastmessage = 'not empty'

# recieve buffer
rcv_buf = []

# send buffer
snd_buf = []

synFormat = "SYN\nSequence: 0\nLength: 0\n\n"
synResp = "ACK\nWindow: 1024\nAcknowlegment: 100\n\n"

datFormat = "DAT\nSequence: 100\nLength: 100\n\n/.*"
datResp = "ACK\nWindow: 924\nAcknowlegment: 200\n\n"

# put syn packet in send buffer
snd_buf.append(synFormat)

# send encoded packet
udp_sock.sendto(synFormat.encode(), server_address)

continueLoop = True

while continueLoop:

    # Wait for at least one of the sockets to be
    # ready for processing
#    print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,
                                                    outputs,
                                                    inputs,
                                                    timeout)

    # Handle inputs


    if udp_sock in readable:
        # recieve data and append to rcv_buf
        packet = snd_buf.pop(0)
        rcv_buf.append(packet) 

        # if message cannot be recognized:s
            
                # write rst packet into snd_buf

        # if end of message
        if (packet[-2:] == "\n\n"):
            
            # split the packet
            RDP = packet.split("\n")
            
            # check if its SYN
            if RDP[0] == 'SYN':
                print('tru')

        continueLoop = False






    # Handle outputs
    for udpSocket in writable:
        x = 1
        # bytes_sent = udp_sock.send(snd_buf)
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
