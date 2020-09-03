import logging
import socket
import struct
from contextlib import contextmanager
from typing import Optional, ContextManager


logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(name)s: %(message)s', level = logging.DEBUG)
logger = logging.getLogger(__name__)

class BaseConnection:

    def __init__(self, socket_ = None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if socket_ is None else socket_

    @classmethod
    def create_from(cls, socket_) -> 'BaseConnection':
        return cls(socket_ = socket_)

    def send_message(self, message: bytes) -> None:
        # ADAPTED FROM: https://stackoverflow.com/a/17668009/2553200
        # Prefix each message with a 4-byte length (network byte order)
        message = struct.pack('>I', len(message)) + message
        self.socket.sendall(message)

    def receive_message(self) -> Optional[bytes]:
        # ADAPTED FROM: https://stackoverflow.com/a/17668009/2553200
        # Read message length and unpack it into an integer
        raw_message_length: bytes = self.recvall(4)

        if not raw_message_length:
            return None

        message_length, = struct.unpack('>I', raw_message_length)

        # Read the message data
        return self.recvall(message_length)

    def recvall(self, n: int) -> bytes:
        # ADAPTED FROM: https://stackoverflow.com/a/17668009/2553200
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data


class ClientConnection(BaseConnection):

    @contextmanager
    def __call__(self, server_address: tuple) -> ContextManager[BaseConnection]:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(server_address)
            logger.info(f'Client is connected to {server_address[0]}:{server_address[1]}')
            yield self
        finally:
            self.socket.close()
