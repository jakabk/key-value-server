from key_value_server.communication import Response, Status, Operation, Request


def test_response_serialize():
    response = Response(Status.NOT_FOUND, {'key': 'keyA'})
    assert response.serialize() == b'["not_found", {"key": "keyA"}]'


def test_request_serialize():
    request = Request(Operation.RETRIEVE, {'key': 'keyA'})
    assert request.serialize() == b'["retrieve", {"key": "keyA"}]'


def test_response_from_raw():
    response = Response.from_raw(b'["found", {"prefix": ["keyA", "keyB"]}]')

    assert response.info == Status.FOUND
    assert response.data['prefix'] == ['keyA', 'keyB']


def test_request_from_raw():
    test_data = {"key": "keyA", "value": "valueA"}
    request = Request.from_raw(b'["store", {"key": "keyA", "value": "valueA"}]')

    assert request.info == Operation.STORE
    assert request.data.keys() == test_data.keys()
    assert list(request.data.values()) == list(test_data.values())
