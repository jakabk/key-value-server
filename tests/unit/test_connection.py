from key_value_server.connection import BaseConnection


class BasicSocketMock:

    def __init__(self):
        self._data = b''

    def sendall(self, message):
        self._data = message

    def recv(self, n):
        if n > len(self._data):
            data = self._data[:]
            self._data = b''
            return data

        receive = self._data[:n]
        self._data = self._data[n:]
        return receive


def test_connection_send_message():
    message = b'["store", {"key": "keyA", "value": "valueA"}]'

    socket = BasicSocketMock()
    connection = BaseConnection(socket)
    connection.send_message(message)

    assert socket._data == b'\x00\x00\x00-["store", {"key": "keyA", "value": "valueA"}]'


def test_connection_receive():
    message = b'["store", {"key": "keyA", "value": "valueA"}]'

    socket = BasicSocketMock()
    connection = BaseConnection(socket)
    connection.send_message(message)

    result = connection.receive_message()

    assert result == message
