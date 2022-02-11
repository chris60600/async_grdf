""" Grdf Api Exceptions """


class GrdfApiError(Exception):
    """Generic GrdfApi exception."""


class GrdfApiDecodeError(GrdfApiError):
    """GrdfApi exception thrown when decoding a response fails."""

    def __init__(self, message, raw_body):
        """Init Decode error."""
        super().__init__(message)
        self.raw_body = raw_body

    def get_raw_body(self) -> str:
        """Return the raw body of the failing request."""
        return self.raw_body


class GrdfApiEmptyResponseError(GrdfApiError):
    """GrdfApi empty API response exception."""


class GrdfApiConnectionError(GrdfApiError):
    """GrdfApi connection exception."""


class GrdfApiConnectionTimeoutError(GrdfApiConnectionError):
    """GrdfApi connection Timeout exception."""