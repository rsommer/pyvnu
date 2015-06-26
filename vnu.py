# coding: utf-8
"""A requests-based interface to the `validator.nu`_ service.

This module provides access to the functionality provided by `validator.nu`_ or
a private instance of it.

.. _validator.nu:
   https://validator.nu/
"""
import requests as _requests


class HTML5Validator(object):
    """HTML5 validator.

    Attributes:
        validator_url (str): The http endpoint. Defaults to https://validator.nu/.
        fragment_prefix (str): HTML5 boilerplate start. Used for fragment checking.
        fragment_suffix (str): HTML5 boilerplate end. Used for fragment checking.
        fragment_template (str): String template for HTML5 fragments.
            Used to surround a fragment with minimal HTML5 boilerplate.
    """
    validator_url = "https://validator.nu/"

    # Template to allow checking of HTML5 framents
    fragment_prefix = "<!DOCTYPE html><html><head><title>Fragent</title></head><body>"
    fragment_suffix = "</body></html>"
    fragment_template = fragment_prefix + "{fragment}" + fragment_suffix

    def __init__(
        self,
        validator_url=None,
        out="json",
        asciiquotes="yes",
        laxtype="yes",
        content_type="text/html",
        charset="utf-8"
    ):
        """Initialize validator class.

        Args:
            validator_url (Optional[str]): URL, overrides default http endpoint.
            out (Optional[str]): Set output type. Defaults to "json".
                Supported output types are "json" and "text".
            asciiquotes (Optional[str]): Use asciiquotes in output. Defaults to "yes".
                Can be one of "yes" or "no".
            laxtype (Optional[str]): Configure RelaxNG usage.
            content_type (Optional[str]): Defaults to "text/html".
            charset (Optional[str]): Defaults to "utf-8".
        """

        if validator_url is not None:
            self.validator_url = validator_url
        self.session = _requests.Session()
        self.session.headers.update(
            {"content-type": "{0}; charset={1}".format(content_type, charset)}
        )
        self.params = {
            "out": out,
            "laxtype": laxtype,
            "asciiquotes": asciiquotes,
        }

    @staticmethod
    def _handle_json(response):
        """Handle json response.

        Args:
            response (requests.Reponse): The validator's response.

        Returns:
            A tuple representing the http status and the decoded response:

            (
              200,
              {u'messages':
                [
                  {
                    u'message': u'Message text',
                    u'type': u'info'
                  },
                  {
                    u'message': u'Error description',
                    u'type': u'error'
                  }
                ]
              }
            )
        """
        return response.status_code, response.json()

    @staticmethod
    def _handle_text(response):
        """Handle text response.

        Args:
            response (requests.Reponse): The validator's response.

        Returns:
            A tuple representing the http status and the response text.
        """
        return response.status_code, response.text

    def _prepare(self, params=None):
        request_params = self.params.copy()

        if params:
            request_params.update(params)

        handler = getattr(self, "_handle_{0}".format(request_params.get("out")))

        return handler, request_params

    def validate_fragment(self, fragment, params=None):
        """Validate a HTML5 fragment.

        In order to be able to validate just a fragment, the given piece of text
        is wrapped into minimal HTML5 boilerplate.

        Args:
            fragment (str): A HTML5 fragment.
            params (Optional[dict]): Parameter override. Defaults to None.
        """
        return self.validate_document(
            self.fragment_template.format(fragment=fragment),
            params=params
        )

    def validate_document(self, document, params=None):
        """Validate a full HTML5 document.

        Args:
            document (str): The full document.
            params (Optional[dict]): Parameter override. Defaults to None.
        """
        handler, request_params = self._prepare(params)

        return handler(
            self.session.post(
                self.validator_url,
                params=request_params,
                data=document,
            )
        )

    def validate_file(self, fileinput, params=None):
        """Validate a (local) file.

        Args:
            fileinput (str of file): Filename or file-like object.
            params (Optional[dict]): Parameter override. Defaults to None.
        """
        handler, request_params = self._prepare(params)

        if isinstance(fileinput, basestring):
            fileinput = open(fileinput)

        return handler(
            self.session.post(
                self.validator_url,
                params=request_params,
                data=fileinput,
            )
        )

    def validate_url(self, url, params=None):
        """Validate given URL.

        The URL must be reachable by the configured validation service.

        Args:
            url (str): URL to validate
            params (Otional[dict]): Parameter override. Defaults to None.
        """
        handler, request_params = self._prepare(params)
        request_params.update({"doc": url})

        return handler(
            self.session.get(
                self.validator_url,
                params=request_params,
            )
        )

    def validate(self, to_validate, params=None):
        """Validate given input (trying to guess what it is).

        Args:
            to_validate (str or filelike): Validation input
                Depending on input, the real validation handler is guessed.
            params (Optional[dict]): Parameter override. Defaults to None.

        Returns:
            tuple of (status_code, response_obj). response_obj depends on out param.
        """
        if "://" in to_validate:  # assume URL
            return self.validate_url(to_validate, params=params)
        elif "<" in to_validate:  # assume html5
            if to_validate.lower().startswith("<!doctype"):  # assume full document
                return self.validate_document(to_validate, params=params)
            else:  # assume html fragment
                return self.validate_fragment(to_validate, params=params)
        else:  # assume file-ish thing
            return self.validate_file(to_validate, params=params)
