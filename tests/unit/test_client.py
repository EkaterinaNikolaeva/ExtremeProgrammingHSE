import pytest
from unittest import mock
from lib.client import add_key_value, get_key

storage = {}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200 and self.status_code != 201:
            raise Exception("bad status")


def mock_add_key_value(*args, **kwargs):
    key = kwargs["json"]["key"]
    value = kwargs["json"]["value"]
    storage[key] = value
    return MockResponse({}, 201)


def mock_get_value(*args, **kwargs):
    key = kwargs["params"]["key"]
    if key not in storage:
        return MockResponse({}, 404)
    return MockResponse({"value": storage[key]}, 200)


@mock.patch("requests.put", mock_add_key_value)
@mock.patch("requests.get", mock_get_value)
@pytest.mark.parametrize(
    "key, value",
    [("a", "b"), ("aba", "caba"), ("x", "y")],
)
def test_storage(key, value):
    add_key_value(key=key, value=value)
    assert value == get_key(key)
