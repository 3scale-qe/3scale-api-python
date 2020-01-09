import logging
from typing import Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def extract_response(response: requests.Response, entity: str = None,
                     collection: str = None) -> Union[dict, list]:
    """Extract the response from the response
    Args:
        response(requests.Response): Response
        entity(str): entity name to be extracted
        collection(str): collection name to be extracted
    Returns(Union[dict, list]): Extracted entity or list of entities
    """
    extracted: dict = response.json()
    if collection and collection in extracted:
        extracted = extracted.get(collection)
    if isinstance(extracted, list):
        return [value.get(entity) for value in extracted]
    if entity in extracted.keys():
        return extracted.get(entity)
    return extracted


class HttpClient:
    """3scale specific!!! HTTP Client

    This provides client to easily run api calls against provided service.
    Due to some delays in the infrastructure the client is configured to retry
    calls under certain conditions. To modify this behavior customized session
    has to be passed. session has to be fully configured in such case
    (e.g. including authentication"

    :param app: Application for which client should do the calls
    :param endpoint: either 'sandbox_endpoint' (staging) or 'endpoint' (production),
        defaults to sandbox_endpoint
    :param session: Used instead of default; it has to be fully configured
    :param verify: SSL verification
    """

    def __init__(self, app, endpoint: str = "sandbox_endpoint",
                 session: requests.Session = None, verify: bool = None):
        self._app = app
        self._endpoint = endpoint
        if session is None:
            session = requests.Session()
            self.retry_for_session(session)

            session.auth = app.authobj

        if verify is not None:
            session.verify = verify

        self._session = session

        logger.debug("[HTTP CLIENT] New instance: %s", self._base_url)

    @staticmethod
    def retry_for_session(session: requests.Session, total: int = 8):
        retry = Retry(
            total=total,
            backoff_factor=1,
            status_forcelist=(503, 404),
            raise_on_status=False,
            respect_retry_after_header=False
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

    @property
    def _base_url(self) -> str:
        """Determine right url at runtime"""
        return self._app.service.proxy.fetch()[self._endpoint]

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """mimics requests interface"""
        url = urljoin(self._base_url, path)

        logger.debug("[%s] (%s) %s", method, url, kwargs or "")
        response = self._session.request(method=method, url=url, **kwargs)
        return response

    def get(self, *args, **kwargs) -> requests.Response:
        """mimics requests interface"""
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        """mimics requests interface"""
        return self.request('POST', *args, **kwargs)

    def patch(self, *args, **kwargs) -> requests.Response:
        """mimics requests interface"""
        return self.request('PATCH', *args, **kwargs)

    def put(self, *args, **kwargs) -> requests.Response:
        """mimics requests interface"""
        return self.request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs) -> requests.Response:
        """mimics requests interface"""
        return self.request('DELETE', *args, **kwargs)
