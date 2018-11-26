#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Client UDP implement a socket to a register server."""

import socket
import sys

# Client UDP simple.

# Pick method, ip address, login and port of keyboard.
try:
    METHOD = sys.argv[1]
    SERVER = sys.argv[2].split('@')[1].split(':')[0]
    LOGIN = sys.argv[2].split('@')[0]
    PORT = int(sys.argv[2].split(':')[1])
except (IndexError, ValueError):
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

# Content to send
LINE = METHOD + ' sip:' + LOGIN + '@' + SERVER + ' SIP/2.0\r\n'

# Create the socket, configure it and attach it to server/port
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print('Sending: ' + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    response = data.decode('utf-8')
    print(response)
    if response.split()[1] == '100':
        ack = 'ACK sip:' + LOGIN + '@' + SERVER + ' SIP/2.0\r\n'
        my_socket.send(bytes(ack, 'utf-8') + b'\r\n')
        print('Sending: ' + ack)
    print('Ending socket...')

print('Socket done.')
