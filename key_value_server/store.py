import logging
from functools import wraps
from typing import Generator

import pickledb

from key_value_server.communication import Response, Status

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(name)s: %(message)s', level = logging.DEBUG)
logger = logging.getLogger(__name__)

def handle_result(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            status, result = func(*args, **kwargs)
            return Response(status, result)
        except Exception as exc:
            return Response(Status.ERROR, {'error': f'{type(exc)}: {exc}'})

    return wrapper


class Store:

    def __init__(self, dbpath: str = '/tmp/key-value.db', auto_dump: bool = True):
        self._store: pickledb.PickleDB = pickledb.load(dbpath, auto_dump)

    @handle_result
    def store(self, data: dict) -> Response:
        """Storing a value: the client sends the key and the value for the server."""
        status = Status.UPDATED if self._store.exists(data['key']) else Status.CREATED
        self._store.set(**data)
        logger.debug(f'{"Created" if status is Status.CREATED else "Updated"}: {data}')
        return status, {}

    @handle_result
    def retrieve(self, data: dict) -> Response:
        """Retrieving a value: the client specifies the key, and the server must reply with the value associated to it.
        If there's no value associated with the specified key, then the server return a message indicating this."""
        if not self._store.exists(data['key']):
            logger.debug(f'Not found: {data}')
            return Status.NOT_FOUND, {'key': data['key']}

        logger.debug(f'Found: {data}')
        return Status.FOUND, {'result': self._store.get(data['key'])}

    @handle_result
    def find(self, data: dict) -> Response:
        """Finding a value: the client specifies a prefix.
        The server returns all the keys whose value starts with the prefix specified by the client."""
        keys = list(self._find(data['prefix']))
        if keys:
            return Status.FOUND, {'result': keys}

        logger.debug(f'{"Found" if keys else "Not found"}: {data}')
        return Status.NOT_FOUND, {'prefix': data['prefix']}

    def _find(self, prefix) -> Generator:
        for key, value in self._store.db.items():
            if value.startswith(prefix):
                yield key
