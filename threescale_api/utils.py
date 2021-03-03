import logging
import shlex
from typing import Union, Iterable
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
    :param verify: SSL verification
    :param cert: path to certificate
    :param disable_retry_status_list:
        Iterable collection of status code that should not be retried by requests
    """

    def __init__(self, app, endpoint: str = "sandbox_endpoint",
                 verify: bool = None, cert=None, disable_retry_status_list: Iterable = ()):
        self._app = app
        self._endpoint = endpoint
        self.verify = verify if verify is not None else app.api_client_verify
        self.cert = cert
        self._status_forcelist = {503, 404} - set(disable_retry_status_list)
        self.auth = app.authobj()
        self.session = self._create_session()

        logger.debug("[HTTP CLIENT] New instance: %s", self._base_url)

    def close(self):
        """Close requests session"""
        self.session.close()

    @staticmethod
    def retry_for_session(session: requests.Session, status_forcelist: Iterable, total: int = 8):
        retry = Retry(
            total=total,
            backoff_factor=1,
            status_forcelist=status_forcelist,
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

    def _create_session(self):
        """Creates session"""
        session = requests.Session()
        self.retry_for_session(session, self._status_forcelist)
        return session

    def extend_connection_pool(self, maxsize: int):
        """Extend connection pool"""
        self.session.adapters["https://"].poolmanager.connection_pool_kw["maxsize"] = maxsize
        self.session.adapters["https://"].poolmanager.clear()

    def request(self, method, path,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, json=None) -> requests.Response:
        """mimics requests interface"""
        url = urljoin(self._base_url, path)
        session = self.session
        session.auth = auth or self.auth

        req = requests.Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        prep = session.prepare_request(req)

        logger.info("[CLIENT]: %s", request2curl(prep))

        send_kwargs = {
            "timeout": timeout,
            "allow_redirects": allow_redirects
        }

        proxies = proxies or {}

        send_kwargs.update(
            session.merge_environment_settings(prep.url, proxies, stream, self.verify, self.cert))

        response = session.send(prep, **send_kwargs)

        logger.info("\n".join(["[CLIENT]:", response2str(response)]))

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


def request2curl(request: requests.PreparedRequest) -> str:
    """Create curl command corresponding to given request"""

    cmd = ["curl", "-X %s" % shlex.quote(request.method)]
    if request.headers:
        cmd.extend([
            "-H %s" % shlex.quote(f"{key}: {value}")
            for key, value in request.headers.items()])
    if request.body:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        cmd.append("-d %s" % shlex.quote(body))
    cmd.append(shlex.quote(request.url))

    return " ".join(cmd)


def response2str(response: requests.Response):
    """Return string representation of requests.Response"""

    # Let's cheat with protocol, hopefully no-one will ever notice this ;)
    msg = [f"HTTP/1.1 {response.status_code} {response.reason}"]
    for key in response.headers:
        msg.append(f"{key}: {response.headers[key]}")
    msg.append("")
    body = response.text
    if len(body) > 160:
        body = body[:160] + "..."
    msg.append(body)
    return "\n".join(msg)
