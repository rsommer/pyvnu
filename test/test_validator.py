# coding: utf-8
import os as _os
import pytest as _pytest
import mock as _mock
import cStringIO as _StringIO

import vnu as _vnu


BASEDIR = _os.path.abspath(_os.path.dirname(__file__))
SUPPORTED_OUTPUTS = ["json", "text"]


@_pytest.fixture
def validator():
    return _vnu.HTML5Validator()


@_pytest.mark.parametrize("url", ["http://test01", "http://test02"])
def test_service_config(url):
    service = _vnu.HTML5Validator(url)
    assert service.validator_url == url


@_pytest.mark.parametrize("out", SUPPORTED_OUTPUTS)
def test_output_modes(validator, out):
    status, output = validator.validate_fragment("<div></div>", params={"out": out})
    assert status == 200
    if out == "json":
        assert all([msg["type"] == "info" for msg in output["messages"]])
    else:
        assert output


def test_valid_fragment(validator):
    status, output = validator.validate_fragment("<div></div>")
    assert status == 200
    assert all([msg["type"] == "info" for msg in output["messages"]])


def test_valid_unicode_fragment(validator):
    status, output = validator.validate_fragment(u"<div>öüä</div>")
    assert status == 200
    assert all([msg["type"] == "info" for msg in output["messages"]])


def test_invalid_fragment(validator):
    status, json = validator.validate_fragment("<div></vid>")
    assert status == 200
    assert any([msg["type"] == "error" for msg in json["messages"]])


def test_invalid_document(validator):
    status, json = validator.validate_document("<!doctype html><div></vid>")
    assert status == 200
    assert any([msg["type"] == "error" for msg in json["messages"]])


def test_invalid_unicode_document(validator):
    status, json = validator.validate_document(u"<!doctype html><div>öüä</vid>")
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


def test_validate_url(validator):
    status, json = validator.validate_url(validator.validator_url)
    assert status == 200
    assert "messages" in json


def test_validate_guess_fragment(validator):
    validator.validate_fragment = _mock.MagicMock()
    validator.validate("<div></div>")
    validator.validate_fragment.assert_called_once()


def test_validate_guess_document(validator):
    validator.validate_document = _mock.MagicMock()
    validator.validate("<!doctype html><div></div>")
    validator.validate_document.assert_called_once()


def test_validate_guess_filename(validator):
    validator.validate_file = _mock.MagicMock()
    validator.validate("testdata/test.html")
    validator.validate_file.assert_called_once()


def test_validate_guess_url(validator):
    validator.validate_url = _mock.MagicMock()
    validator.validate(validator.validator_url)
    validator.validate_url.assert_called_once()
