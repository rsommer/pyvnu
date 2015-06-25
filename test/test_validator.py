# coding: utf-8
import os as _os
import pytest as _pytest
import cStringIO as _StringIO

import vnu as _vnu


BASEDIR = _os.path.abspath(_os.path.dirname(__file__))


@_pytest.fixture
def validator():
    return _vnu.HTML5Validator()


def test_valid_fragment(validator):
    status, json = validator.validate_fragment("<div></div>")
    assert status == 200
    assert all([msg["type"] == "info" for msg in json["messages"]])


def test_invalid_fragment(validator):
    status, json = validator.validate_fragment("<div></vid>")
    assert status == 200
    assert any([msg["type"] == "error" for msg in json["messages"]])


def test_valid_file_from_name(validator):
    testfile = _os.path.join(BASEDIR, "valid.html")
    status, json = validator.validate_file(testfile)
    assert status == 200
    assert all([msg["type"] == "info" for msg in json["messages"]])


def test_invalid_file_from_name(validator):
    testfile = _os.path.join(BASEDIR, "invalid.html")
    status, json = validator.validate_file(testfile)
    assert status == 200
    assert any([msg["type"] == "error" for msg in json["messages"]])


def test_valid_file_from_fileobj(validator):
    html = "<!doctype html><html><head><title>Valid test</title></head><body></body></html>"
    status, json = validator.validate_file(
        _StringIO.StringIO(html)
    )
    assert status == 200
    assert all([msg["type"] == "info" for msg in json["messages"]])


def test_invalid_file_from_fileobj(validator):
    html = "<!doctype html><html><head><title>Valid test</title></head><vid></div></body></html>"
    status, json = validator.validate_file(
        _StringIO.StringIO(html)
    )
    assert status == 200
    assert any([msg["type"] == "error" for msg in json["messages"]])
