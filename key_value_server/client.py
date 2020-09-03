import logging

from key_value_server.communication import Request, Operation, Response
from key_value_server.connection import ClientConnection

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(name)s: %(message)s', level = logging.DEBUG)
logger = logging.getLogger(__name__)


class Client:

    def __init__(self, host: str, port: int):
        self.server_address = (host, port)

    def store(self, key: str, value: str) -> Response:
        logger.debug(f'Request: store | key: {key} - value: {value}')
        return self._send(
            Request(Operation.STORE, dict(key = key, value = value))
        )

    def retrieve(self, key: str) -> Response:
        logger.debug(f'Request: retrieve | key: {key}')
        return self._send(
            Request(Operation.RETRIEVE, dict(key = key))
        )

    def find(self, prefix: str) -> Response:
        logger.debug(f'Request: find | prefix: {prefix}')
        return self._send(
            Request(Operation.FIND, dict(prefix = prefix))
        )

    def _send(self, request: Request) -> Response:
        connection = ClientConnection()

        with connection(self.server_address) as server_connection:
            server_connection.send_message(request.serialize())
            raw_response = server_connection.receive_message()

            return Response.from_raw(raw_response)
