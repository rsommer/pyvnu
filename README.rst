=====
pyvnu
=====

A simple client for the `validator.nu`_ validation service.

.. _validator.nu: https://validator.nu/

Installation
------------

To install just do: ::

    python setup.py install

There is no package on PyPI yet.

Basic Use
---------

To use the client from your python project: ::

    import vnu

    validator = vnu.HTML5Validator()
    status, response = validator.validate("<div></div>")

The `validator.validate()` call tries to guess what you are trying to validate.
This could be a HTML5 fragment, a complete HTML5 document, an URL or a local file
given as a filename or a file-like object.

You can call the underlying methods directly: ::

    validator.validate_fragment("<div></div>")
    validator.validate_document("<!doctype html><html>...</html>")
    validator.validate_file("filename.html")
    validator.validate_file(open("filename.html"))
    validator.validate_url("https://google.com/")

The `validator.validate_fragment()` call wraps the given fragment into HTML5
boilerplate in order to be able to validate it.

To validate a page from the commandline: ::

    vnu https://www.google.de/
