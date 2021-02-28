import socket
import sys

import patterns

HOST = 'localhost'
PORT = 12346


class IRCServer(patterns.Subscriber):


                conn.sendall(b'ok')
                print(data.decode('utf-8'))


def run_receiver(self):
    while True:
        try:
            # check for input messages
            any_message, _, _ = select.select(
                [self.sock], [], [], 0
            )
            if any_message:
                data = self.sock.recv(1024)
                print(data.decode('utf-8'))
            await asyncio.sleep(0.05)
            # detect message type and process it
            # send output messages per client instance
            # while self.msg:
            #    item = self.msg.pop(0)
            #    self.send_msg(item.encode())
            # PING - PONG
            for client in self.subscribers:
                while client.msg:
                    item = client.msg.pop(0)
                    self.send_msg(item.encode())

        except socket.error:
            # KeyboardInterrupt signifies the end of the view
            logger.debug(f"KeyboardInterrupt detected within the view")
            raise


def run_connect(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    with view.View() as v:
                        logger.info(f"Entered the context of a View object")
                        self.add_subscriber(client)
                        logger.debug(f"Client is subscribed to the View (to receive user input)")
            except socket.error:
                # KeyboardInterrupt signifies the end of the view
                logger.debug(f"KeyboardInterrupt detected within the view")
                raise


def main(args):
    # Pass your arguments where necessary
    logger.info(f"Server object created")

    async def inner_run():
        await asyncio.gather(
            self.run_receiver(),
            self.run_connect(),
            return_exceptions=True,
        )
    try:
        asyncio.run(inner_run())
    except KeyboardInterrupt as e:
        logger.debug(f"Signifies end of process")
    client.close()