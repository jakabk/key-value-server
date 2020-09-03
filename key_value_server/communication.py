import json
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    CREATED = "created"
    UPDATED = "updated"
    FOUND = "found"
    NOT_FOUND = "not_found"
    ERROR = "error"


class Operation(Enum):
    STORE = "store"
    RETRIEVE = "retrieve"
    FIND = "find"


class CommunicationBase:

    def serialize(self) -> bytes:
        # print("SERIALIZE", self.info, self.data)
        return json.dumps((self.info.value, self.data)).encode('utf-8')

    @classmethod
    def from_raw(cls, raw: bytes) -> "CommunicationBase":
        info, data = json.loads(raw.decode('utf-8'))

        return cls(cls._info_cls(info), data)

    def __str__(self):
        return f'{self.info.value} - {self.data}'


@dataclass
class Response(CommunicationBase):
    info: Status
    data: dict

    _info_cls = Status


@dataclass
class Request(CommunicationBase):
    info: Operation
    data: dict

    _info_cls = Operation
