#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    #FICH = sys.argv[3]
except (IndexError, ValueError):
    sys.exit('Usage: python3 server.py IP port audio_file')




class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    def invite_request(self, mess):
        print(mess)


    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
        received_mess = []
        for index, line in enumerate(self.rfile):
            received_mess = line.decode('utf-8')
            if index == 0:
            # Leyendo línea a línea lo que nos envía el cliente
                print("El cliente nos manda " + received_mess)
                method = received_mess.split()[0]
                if method = 'INVITE':
                    invite_request(received_mess.split()[1].split()[0])
                else:
                    

            else:
                # Si no hay más líneas salimos del bucle infinito
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((SERVER, PORT), EchoHandler)
    print('Listening...')
    serv.serve_forever()
