import logging
import socket

from key_value_server.communication import Request
from key_value_server.connection import BaseConnection
from key_value_server.store import Store

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(name)s: %(message)s', level = logging.DEBUG)
logger = logging.getLogger(__name__)


class Server:

    def __init__(self, host: str, port: str, store: Store):
        self.server_address: tuple = (host, port)
        self.store = store

    def run(self) -> None:
        connection = BaseConnection()
        connection.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.socket.bind(self.server_address)
        connection.socket.listen(1)
        logger.info('Key-value server is listening')

        while True:
            client_socket, client_address = connection.socket.accept()

            with client_socket:
                client_connection = BaseConnection(socket_ = client_socket)
                raw_request = client_connection.receive_message()

                request = Request.from_raw(raw_request)
                client_connection.send_message(getattr(self.store, request.info.value)(request.data).serialize())
