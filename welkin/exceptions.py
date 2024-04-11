from __future__ import annotations

import contextlib
import json

from requests import HTTPError


class WelkinHTTPError(HTTPError):
    """An HTTP error occurred.

    https://developers.welkinhealth.com/#errors
    """

    def __init__(self, exc):
        """WelkinHTTPError constructor.

        Parses out error information from the error object and passes on to the
        :obj:`HTTPError` constructor.

        Args:
            exc (:obj:`HTTPError`): Original exception.
        """
        request = exc.request
        response = exc.response
        msg = exc.args[0]

        with contextlib.suppress(json.JSONDecodeError):
            msg = f"{msg}\n{json.dumps(response.json(), indent=2)}"

        super(HTTPError, self).__init__(msg, request=request, response=response)
