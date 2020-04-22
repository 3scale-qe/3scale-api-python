from threescale_api.utils import request2curl


def test_request2curl():
    URL = "http://example.invalid"
    HEADERS = {"X-Header": "this"}
    HEADERS_STR = "-H 'X-Header: this'"
    DATA = {'key': 'value'}
    BODY_STR = "-d key=value"

    request = _Request("GET", URL, None, None)
    assert request2curl(request) == f"curl -X GET {URL}"

    request = _Request("GET", URL, HEADERS, None)
    assert request2curl(request) == f"curl -X GET {HEADERS_STR} {URL}"

    request = _Request("POST", URL, HEADERS, DATA)
    assert request2curl(request) == f"curl -X POST {HEADERS_STR} {BODY_STR} {URL}"

    request = _Request("PUT", URL, None, DATA, True)
    assert request2curl(request) == f"curl -X PUT {BODY_STR} {URL}"


class _Request:
    def __init__(self, method, url, headers, data, encode=False):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = None
        if data:
            self.body = "&".join([f"{key}={value}" for key, value in data.items()])
        if encode and self.body:
            self.body = self.body.encode("utf-8")
