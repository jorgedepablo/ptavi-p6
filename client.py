#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
try:
    METHOD = sys.argv[1]
    SERVER = sys.argv[2].split('@')[1].split(':')[0]
    LOGIN = sys.argv[2].split('@')[0]
    PORT = int(sys.argv[2].split(':')[1])
except (IndexError, ValueError):
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

# Contenido que vamos a enviar
LINE = METHOD + ' sip:' + LOGIN + '@' + SERVER + ' SIP/2.0\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print('Enviando: ' + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    response = data.decode('utf-8')
    if response.split()[1] == '100':
        ack ='ACK sip:' + LOGIN + '@' + SERVER + ' SIP/2.0\r\n'
        my_socket.send(bytes(ack, 'utf-8') + b'\r\n')
    else:
        print(response)
    print('Terminando socket...')

print('Fin.')
