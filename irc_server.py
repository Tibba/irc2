import socket
import sys

import patterns

HOST = 'localhost'
PORT = 12345


class IRCServer(patterns.Publisher):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(10)
        while True:
            conn, addr = s.accept()

            with conn:
                print('Connected by', addr)

                data = conn.recv(1024)
                if not data: continue
                conn.sendall(data)
                print(data.decode('utf-8'))