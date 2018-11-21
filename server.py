#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Class (and main program) for echo register server in UDP simple."""

import socketserver
import sys
import os

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    FICH = sys.argv[3]
except (IndexError, ValueError):
    sys.exit('Usage: python3 server.py IP port audio_file')


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class"""

    def check_request(self, mess):
        # check if the SIP request is correctly formed
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
        if body.split(':')[1].startswith(':'):
            self.correct = False
        return self.correct

    def handle(self):
        # Handle method of the server class.
        received_mess = []
        for index, line in enumerate(self.rfile):
            received_mess = line.decode('utf-8')
            if index == 0:
            # Reading the first string that client send
                client = received_mess.split(':')[1].split('@')[0]
                print(client + ' send: '+ received_mess)
                if self.check_request(received_mess):
                    method = received_mess.split()[0]
                    if method == 'INVITE':
                        self.wfile.write(b'SIP/2.0 100 Trying\r\n\r\n' +
                                         b'SIP/2.0 180 Ring\r\n\r\n' +
                                         b'SIP/2.0 200 OK\r\n\r\n')
                        print('Sending 100 Trying')
                        print('Sending 180 Ring')
                        print('Sending 200 OK')
                    elif method == 'BYE':
                        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                        print('Sending 200 OK')
                    elif method == 'ACK':
                        ToRun = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + FICH
                        print('Running: ', ToRun)
                        os.system(ToRun)
                    else:
                        self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
                        print('Sending 405 Method Not Allowed')
                else:
                    self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')
                    print('Sending 400 Bad Request')
            else:
            # if no more lines, exit of the loop.
                break

if __name__ == "__main__":
    # Create echo server and listening
    serv = socketserver.UDPServer((SERVER, PORT), EchoHandler)
    print('Listening...')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('  Server interrupt')
