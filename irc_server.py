import socket
import sys

import patterns

HOST = 'localhost'
PORT = 12346


class IRCServer(patterns.Subscriber):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    continue
                conn.sendall(b'ok')
                print(data.decode('utf-8'))