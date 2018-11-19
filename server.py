#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os
import string

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    FICH = sys.argv[3]
except (IndexError, ValueError):
    sys.exit('Usage: python3 server.py IP port audio_file')


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def check_request(self, mess):
        body = mess.split()[1]
        version = mess.split()[2]
        self.correct = True
        if len(mess.split()) != 3:
            self.correct = False
        if version != 'SIP/2.0':
            self.correct = False
        if body.find('@') == -1:
            self.correct = False
        if body.split(':')[0] != 'sip':
            self.correct = False
        return self.correct

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        received_mess = []
        for index, line in enumerate(self.rfile):
            received_mess = line.decode('utf-8')
            if index == 0:
            # Leyendo primer string que nos envía el cliente
                print("El cliente nos manda " + received_mess)
                if self.check_request(received_mess):
                    method = received_mess.split()[0]
                    if method == 'INVITE':
                        self.wfile.write(b'SIP/2.0 100 Trying\r\n\r\n' +
                                         b'SIP/2.0 180 Ring\r\n\r\n' +
                                         b'SIP/2.0 200 OK\r\n\r\n')
                        print('Envio un 100 Trying')
                        print('Envio un 180 Ring')
                        print('Envio un 200 OK')
                    elif method == 'BYE':
                        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                        print('Envio un 200 OK')
                    elif method == 'ACK':
                        ToRun = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + FICH
                        print('Vamos a ejecutar', ToRun)
                        os.system(ToRun)
                    else:
                        self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
                        print('Envio un 405 Method Not Allowed')
                else:
                    self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')
                    print('Envio un 400 Bad Request')
            else:
            # Si no hay más líneas salimos del bucle infinito
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((SERVER, PORT), EchoHandler)
    print('Listening...')
    serv.serve_forever()
