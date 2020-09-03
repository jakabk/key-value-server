import pathlib
import signal
import time
from subprocess import Popen, PIPE

import pytest

from key_value_server.client import Client
from key_value_server.communication import Status


@pytest.fixture
def server():
    try:
        server_process = Popen([
            'python', f'{pathlib.Path(__file__).absolute().parents[2]}/bin/start-server', '--test'
        ], stdout = PIPE)
    except Exception as exc:
        print('Error', type(exc), str(exc))

    time.sleep(0.5)

    yield

    server_process.send_signal(signal.SIGINT)
    stdout = server_process.communicate()[0]
    print(f'Stdout: {stdout}')


@pytest.fixture
def client():
    return Client('0.0.0.0', 5555)


def test_add_create(server, client):
    result = client.store('keyV', 'valueV')

    assert result.info is Status.CREATED


def test_add_update(server, client):
    client.store('keyV', 'valueV')
    result = client.store('keyV', 'valueW')

    assert result.info is Status.UPDATED


def test_retrieve_not_found(server, client):
    key = 'keyX'

    result = client.retrieve(key)

    assert result.info is Status.NOT_FOUND
    assert result.data['key'] == key


def test_retrieve_found(server, client):
    key = 'keyY'
    value = 'valueY'

    client.store(key, value)
    result = client.retrieve(key)

    assert result.info is Status.FOUND
    assert result.data['result'] == value


def test_find_not_found(server, client):
    prefix = 'xxx'

    result = client.find(prefix)

    assert result.info is Status.NOT_FOUND
    assert result.data['prefix'] == prefix


def test_find_found(server, client):
    prefix = 'yyy'

    client.store('keyA', 'yyy_valueV')
    client.store('keyB', 'yyy_valueV')

    result = client.find(prefix)

    assert result.info is Status.FOUND
    assert result.data['result'] == ['keyA', 'keyB']
