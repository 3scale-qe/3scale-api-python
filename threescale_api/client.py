import logging
from urllib.parse import urljoin

import requests

from threescale_api import errors, resources

log = logging.getLogger(__name__)


class ThreeScaleClient:
    def __init__(self, url: str, token: str, throws: bool = True, ssl_verify: bool = True):
        """Creates instance of the 3scale client
        Args:
            url: 3scale instance url
            token: Access token
            throws: Whether it should throw an error
            ssl_verify: Whether to verify ssl
        """
        self._rest = RestApiClient(url=url, token=token, throws=throws, ssl_verify=ssl_verify)
        self._services = resources.Services(self, instance_klass=resources.Service)
        self._accounts = resources.Accounts(self, instance_klass=resources.Account)
        self._methods = resources.Methods(self, instance_klass=resources.Method)
        self._metrics = resources.Metrics(self, instance_klass=resources.Metric)
        self._tenants = resources.Tenants(self, instance_klass=resources.Tenant)
        self._providers = resources.Providers(self, instance_klass=resources.Provider)
        self._active_docs = resources.ActiveDocs(self, instance_klass=resources.ActiveDoc)
        self._account_plans = resources.AccountPlans(self, instance_klass=resources.AccountPlan)
        self._settings = resources.SettingsClient(self)
        self._admin_portal_auth_provider = resources.AdminPortalAuthenticationProvider(self)
        self._dev_portal_auth_provider = resources.DevPortalAuthenticationProvider(self)


    @property
    def rest(self) -> 'RestApiClient':
        """Get REST api client instance
        Returns(RestApiClient): Rest api client instance
        """
        return self._rest

    @property
    def parent(self) -> 'ThreeScaleClient':
        """Parent is self - the 3scale client
        Returns(ThreeScaleClient):
        """
        return self

    @property
    def threescale_client(self) -> 'ThreeScaleClient':
        """3scale client instance
        Returns(ThreeScaleClient): 3scale client instance
        """
        return self

    @property
    def url(self) -> str:
        """Get tenant url
        Returns(str): URL
        """
        return self._rest.url

    @property
    def admin_api_url(self) -> str:
        """Get admin API url
        Returns(str): URL of the 3scale admin api
        """
        return self.url + "/admin/api"

    @property
    def services(self) -> resources.Services:
        """Gets services client
        Returns(resources.Services): Services client
        """
        return self._services

    @property
    def accounts(self) -> resources.Accounts:
        """Gets accounts client
        Returns(resources.Accounts): Accounts client
        """
        return self._accounts

    @property
    def account_plans(self) -> resources.AccountPlans:
        """Gets accounts client
        Returns(resources.AccountPlans): Account plans client
        """
        return self._account_plans

    @property
    def methods(self) -> resources.Methods:
        """Gets methods client
        Returns(resources.Methods): Methods client
        """
        return self._methods

    @property
    def metrics(self) -> resources.Metrics:
        """Gets metrics client
        Returns(resources.Metrics): Metrics client
        """
        return self._metrics

    @property
    def providers(self) -> resources.Providers:
        """Gets providers client
        Returns(resources.Providers): Providers client
        """
        return self._providers

    @property
    def tenants(self) -> resources.Tenants:
        """Gets tenants client
        Returns(resources.Tenants): Tenants client
        """
        return self._tenants

    @property
    def active_docs(self) -> resources.ActiveDocs:
        """Gets active docs client
        Returns(resources.ActiveDocs): Active docs client
        """
        return self._active_docs

    @property
    def settings(self) -> resources.SettingsClient:
        """Gets settings client
        Returns(resources.SettingsClient): Active docs client
        """
        return self._settings

    @property
    def dev_portal_auth_provider(self) -> resources.DevPortalAuthenticationProvider:
        return self._dev_portal_auth_provider

    @property
    def admin_portal_auth_provider(self) -> resources.AdminPortalAuthenticationProvider:
        return self._admin_portal_auth_provider


class RestApiClient:
    def __init__(self, url: str, token: str, throws: bool = True, ssl_verify: bool = True):
        """Creates instance of the Rest API client
        Args:
            url(str): Tenant url
            token(str): Tenant provider token
            throws(bool): Whether to throw exception
            ssl_verify(bool): Whether to verify the ssl certificate
        """
        self._url = url
        self._token = token
        self._throws = throws
        self._ssl_verify = ssl_verify
        log.debug(f"[REST] New instance: {url} token={token} "
                  f"throws={throws} ssl={ssl_verify}")

    @property
    def url(self) -> str:
        return self._url

    def request(self, method='GET', url=None, path='', params: dict = None,
                headers: dict = None, throws=None, **kwargs):
        """Create new request
        Args:
            method(str): method to be used to create an request
            url(str): url to be used to create new request
            path(str): path to be accessed - if url is not provided
            params(dict): Query parameters
            headers(dict): Headers parameters
            throws(bool): Whether to throw
            **kwargs: Optional args added to request

        Returns:

        """

        full_url = url if url else urljoin(self.url, path)
        full_url = full_url + ".json"
        headers = headers or {}
        params = params or {}
        if throws is None:
            throws = self._throws
        params.update(access_token=self._token)
        log.debug(f"[{method}] ({full_url}) params={params} headers={headers} "
                  f"{kwargs if kwargs else ''}")
        response = requests.request(method=method, url=full_url, headers=headers,
                                    params=params, verify=self._ssl_verify, **kwargs)
        process_response = self._process_response(response, throws=throws)
        return process_response

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)

    def _process_response(self, response: requests.Response, throws=None) -> requests.Response:
        message = f"[RES] Response({response.status_code}): {response.content}"

        if response.ok:
            log.debug(message)
        else:
            log.error(message)
            if throws:
                raise errors.ApiClientError(response.status_code, response.content)

        return response
