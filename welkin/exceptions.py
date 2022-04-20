import json

from requests import HTTPError


class WelkinHTTPError(HTTPError):
    """An HTTP error occurred.

    https://developers.welkinhealth.com/#errors
    """

    def __init__(self, request, response):
        """WelkinHTTPError constructor.

        Parses out error information from the error object and passes on to the
        :obj:`HTTPError` constructor.

        Args:
            exc (:obj:`HTTPError`): Original exception.
        """
        msg = json.dumps(response.json())
        super(HTTPError, self).__init__(msg, request=request, response=response)
