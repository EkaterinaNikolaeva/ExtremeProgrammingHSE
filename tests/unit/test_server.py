from src.server.server import RequestException
import pytest


def test_exception():
    exception = RequestException(201, "Ok")
    assert exception.status_code == 201
    assert exception.message == "Ok"