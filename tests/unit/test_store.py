from key_value_server.communication import Status
from key_value_server.store import Store


def test_store_create():
    data = {"key": "keyA", "value": "valueA"}

    store = Store('/tmp/test.db', False)
    result = store.store(data)

    assert result.info is Status.CREATED
    assert result.data == {}


def test_store_update():
    dataA = {"key": "keyA", "value": "valueA"}
    dataB = {"key": "keyA", "value": "valueB"}

    store = Store('/tmp/test.db', False)
    store.store(dataA)
    result = store.store(dataB)

    assert result.info is Status.UPDATED
    assert result.data == {}


def test_retrieve_not_found():
    data = {'key': 'keyA'}

    store = Store('/tmp/test.db', False)
    result = store.retrieve(data)

    assert result.info is Status.NOT_FOUND
    assert result.data['key'] == data['key']


def test_retrieve_found():
    data = {'key': 'keyA', 'value': 'valueA'}

    store = Store('/tmp/test.db', False)
    store.store(data)
    result = store.retrieve(data)

    assert result.info is Status.FOUND
    assert result.data['result'] == data['value']


def test_find_not_found():
    data = {'prefix': 'xxx'}

    store = Store('/tmp/test.db', False)
    result = store.find(data)
    print(result.info, result.data)

    assert result.info is Status.NOT_FOUND
    assert result.data['prefix'] == data['prefix']


def test_find_found():
    # arrange
    store = Store('/tmp/test.db', False)
    store.store({'key': 'keyA', 'value': 'yyyvalueA'})
    store.store({'key': 'keyB', 'value': 'yyyvalueB'})

    data = {'prefix': 'yyy'}

    # act
    result = store.find(data)
    print(result.info, result.data)

    assert result.info is Status.FOUND
    assert result.data['result'] == ['keyA', 'keyB']


def test_handle_result_error():
    data = {'prefix', 'yyy'}

    store = Store('/tmp/test.db', False)
    result = store.find(data)

    assert result.info is Status.ERROR
    assert result.data['error'] == "<class 'TypeError'>: 'set' object is not subscriptable"
