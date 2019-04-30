import logging
from urllib.parse import urljoin

import requests


logger = logging.getLogger('tests')


class HttpClient:

    def __init__(self, url: str, ssl_verify: bool, params: dict = None) -> None:
        self._url = url
        self._ssl_verify = ssl_verify
        self._session = requests.Session()
        self._params = params or {}
        logger.debug(f"[HTTP CLIENT] New instance: {url} ssl={ssl_verify} params={params}")

    def request(self, method: str, path: str, params: dict = None,
                headers: dict = None, **kwargs) -> requests.Response:
        full_url = urljoin(self._url, path)
        headers = headers or {}
        if params:
            self._params.update(params)
        logger.debug(f"[{method}] ({full_url}) params={self._params} headers={headers} "
                     f"{kwargs if kwargs else ''}")
        response = self._session.request(method=method, url=full_url, headers=headers,
                                         params=self._params, verify=self._ssl_verify, **kwargs)
        return response

    def get(self, *args, **kwargs) -> requests.Response:
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        return self.request('POST', *args, **kwargs)

    def patch(self, *args, **kwargs) -> requests.Response:
        return self.request('PATCH', *args, **kwargs)

    def put(self, *args, **kwargs) -> requests.Response:
        return self.request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs) -> requests.Response:
        return self.request('DELETE', *args, **kwargs)
