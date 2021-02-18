class ThreeScaleApiError(Exception):
    def __init__(self, message, *args):
        self.message = message
        Exception.__init__(self, message, *args)


class ApiClientError(ThreeScaleApiError):
    def __init__(self, code, reason, body, message: str = None):
        self.code = code
        self.reason = reason
        self.body = body
        self._message = message
        msg = f"Response({self.code} {reason}): {body}"
        if message:
            msg += f"; {message}"
        ThreeScaleApiError.__init__(self, msg)
