#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021
#
# Distributed under terms of the MIT license.

"""
Description:

"""
import asyncio
import logging
import select
import threading
from concurrent.futures import thread

import patterns
import view
import socket
import argparse

logging.basicConfig(filename='view.log', level=logging.DEBUG)
logger = logging.getLogger()

# HOST = 'localhost'
# PORT = 12346


class IRCClient(patterns.Subscriber):

    def __init__(self, host, port):
        super().__init__()
        self.username = ""
        self.msg = []
        self._run = True
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, int(port)))

    def set_view(self, view):
        self.view = view

    def update(self, msg):
        # Will need to modify this
        if not isinstance(msg, str):
            raise TypeError(f"Update argument needs to be a string")
        elif not len(msg):
            # Empty string
            return
        logger.info(f"IRCClient.update -> msg: {msg}")
        if not self.username:
            self.username = msg
        else:
            self.process_input(msg)

    def process_input(self, msg):
        # Will need to modify this
        logger.info(f"In process input -> msg: {msg}")
        self.add_msg(msg)
        if msg.lower().startswith('/quit'):
            # Command that leads to the closure of the process
            raise KeyboardInterrupt
        else:
            self.msg.append(msg)
        # self.send_msg(msg)

    def send_msg(self, data):
        self.sock.sendall(bytes(data))

    def add_msg(self, msg):
        self.view.add_msg(self.username, msg)

    def connect(self, username):
        self.sock.connect((HOST, PORT))

    async def run(self):
        """
        Driver of your IRC Client
        """
        self.add_msg("Type your nickname")
        # Remove this section in your code, simply for illustration purposes
        while True:
            try:
                # check for input messages
                any_message, _, _ = select.select(
                    [self.sock], [], [], 0
                )
                if any_message:
                    data = self.sock.recv(1024)
                    self.add_msg(data.decode('utf-8'))
                await asyncio.sleep(0.05)
                # detect message type and process it
                # send output messages
                while self.msg:
                    item = self.msg.pop(0)
                    self.send_msg(item.encode())
                # PING - PONG
            except socket.error:
                # KeyboardInterrupt signifies the end of the view
                logger.debug(f"KeyboardInterrupt detected within the view")
                raise

    def close(self):
        # Terminate connection
        logger.debug(f"Closing IRC Client object")
        pass


def main(args):
    # Pass your arguments where necessary
    client = IRCClient(args[0], args[1])
    logger.info(f"Client object created")
    with view.View() as v:
        logger.info(f"Entered the context of a View object")
        client.set_view(v)
        logger.debug(f"Passed View object to IRC Client")
        v.add_subscriber(client)
        logger.debug(f"IRC Client is subscribed to the View (to receive user input)")

        async def inner_run():
            await asyncio.gather(
                client.run(),
                v.run(),
                return_exceptions=True,
            )
        try:
            asyncio.run(inner_run())
        except KeyboardInterrupt as e:
            logger.debug(f"Signifies end of process")
    client.close()


if __name__ == "__main__":
    # Parse your command line arguments here
    parser = argparse.ArgumentParser()

    parser.add_argument('--server', '-s', default='127.0.0.1', help='server IP address')
    parser.add_argument('-p', '--port', default='12346', help='server port')

    args = parser.parse_args()
    HOST = args.server
    PORT = args.port

    cmdArgs = [HOST, PORT]
    main(cmdArgs)
