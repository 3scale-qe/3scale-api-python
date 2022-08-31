import logging
import time
from urllib.parse import urljoin

import backoff
import requests

from threescale_api import errors, resources

log = logging.getLogger(__name__)


class ThreeScaleClient:
    def __init__(self, url: str, token: str,
                 throws: bool = True, ssl_verify: bool = True, wait: int = -1):
        """Creates instance of the 3scale client
        Args:
            url: 3scale instance url
            token: Access token
            throws: Whether it should throw an error
            ssl_verify: Whether to verify ssl
            wait: Whether to wait for 3scale availability, negative number == no waiting
                positive number == wait another extra seconds
        """
        self._rest = RestApiClient(url=url, token=token, throws=throws, ssl_verify=ssl_verify)
        self._services = resources.Services(self, instance_klass=resources.Service)
        self._accounts = resources.Accounts(self, instance_klass=resources.Account)
        self._provider_accounts = \
            resources.ProviderAccounts(self, instance_klass=resources.ProviderAccount)
        self._provider_account_users = \
            resources.ProviderAccountUsers(self, instance_klass=resources.ProviderAccountUser)
        self._methods = resources.Methods(self, instance_klass=resources.Method)
        self._metrics = resources.Metrics(self, instance_klass=resources.Metric)
        self._analytics = resources.Analytics(self)
        self._tenants = resources.Tenants(self, instance_klass=resources.Tenant)
        self._providers = resources.Providers(self, instance_klass=resources.Provider)
        self._access_tokens = \
            resources.AccessTokens(self, instance_klass=resources.AccessToken)
        self._active_docs = resources.ActiveDocs(self, instance_klass=resources.ActiveDoc)
        self._account_plans = resources.AccountPlans(self, instance_klass=resources.AccountPlan)
        self._settings = resources.SettingsClient(self)
        self._admin_portal_auth_providers = resources.AdminPortalAuthProviders(
            self, instance_klass=resources.AdminPortalAuthProvider)
        self._dev_portal_auth_providers = resources.DevPortalAuthProviders(
            self, instance_klass=resources.DevPortalAuthProvider)
        self._policy_registry = resources.PoliciesRegistry(self,
                                                           instance_klass=resources.PolicyRegistry)
        self._backends = resources.Backends(self, instance_klass=resources.Backend)
        self._webhooks = resources.Webhooks(self)
        self._invoices = resources.Invoices(self, instance_klass=resources.Invoice)
        self._fields_definitions =\
            resources.FieldsDefinitions(self, instance_klass=resources.FieldsDefinition)

        if wait >= 0:
            self.wait_for_tenant()
            # TODO: all the implemented checks aren't enough yet
            # 3scale can still return 404/409 error, therefore slight artificial sleep
            # here to mitigate the problem. This requires proper fix in checks
            time.sleep(wait)

    @backoff.on_predicate(
            backoff.constant, lambda ready: not ready, interval=6, max_tries=90, jitter=None)
    def wait_for_tenant(self) -> bool:
        """
        When True is returned, there is some chance the tenant is actually ready.
        """
        # TODO: checks below were collected from various sources to craft
        # ultimate readiness check. There might be duplicates though, so
        # worth to review it one day
        try:
            return self.account_plans.exists(throws=True) \
                and len(self.account_plans.fetch()["plans"]) >= 1 \
                and len(self.account_plans.list()) >= 1 \
                and self.accounts.exists(throws=True) \
                and len(self.accounts.list()) >= 1 \
                and self.services.exists(throws=True) \
                and len(self.services.list()) >= 1
        except errors.ApiClientError as err:
            if err.code in (404, 409, 503):
                log.info("wait_for_tenant failed: %s", err)
                return False
            raise err
        except Exception as err:
            log.info("wait_for_tenant failed: %s", err)
            return False

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
    def url_with_token(self) -> str:
        return self.rest.url.replace('//', f"//{self.rest._token}@")

    @property
    def token(self) -> str:
        return self.rest._token

    @property
    def admin_api_url(self) -> str:
        """Get admin API url
        Returns(str): URL of the 3scale admin api
        """
        return self.url + "/admin/api"

    @property
    def master_api_url(self) -> str:
        """Get master API url
        Returns(str): URL of the 3scale master api
        """
        return self.url + "/master/api"

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
    def provider_accounts(self) -> resources.ProviderAccounts:
        """Gets provider accounts client
        Returns(resources.ProviderAccouts): Provider Accounts client"""
        return self._provider_accounts

    @property
    def provider_account_users(self) -> resources.ProviderAccountUsers:
        """Gets provider account users client
        Returns(resources.ProviderAccountUsers): Provider Accounts User client
        """
        return self._provider_account_users

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
    def analytics(self):
        """Gets analytics data client
        Returns(resources.Analytics): Analytics client
        """
        return self._analytics

    @property
    def providers(self) -> resources.Providers:
        """Gets providers client
        Returns(resources.Providers): Providers client
        """
        return self._providers

    @property
    def access_tokens(self) -> resources.AccessTokens:
        """Gets AccessTokens client
        Returns(resources.AccessToken): AccessTokens client
        """
        return self._access_tokens

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
    def backends(self) -> resources.Backends:
        """Gets backends client
        Returns(resources.Backends): Backends client
        """
        return self._backends

    @property
    def dev_portal_auth_providers(self) -> resources.DevPortalAuthProviders:
        return self._dev_portal_auth_providers

    @property
    def admin_portal_auth_providers(self) -> resources.AdminPortalAuthProviders:
        return self._admin_portal_auth_providers

    @property
    def policy_registry(self) -> resources.PolicyRegistry:
        return self._policy_registry

    @property
    def webhooks(self) -> resources.Webhooks:
        return self._webhooks

    @property
    def invoices(self) -> resources.Invoices:
        return self._invoices

    @property
    def fields_definitions(self) -> resources.FieldsDefinitions:
        return self._fields_definitions


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
        log.debug("[REST] New instance: %s token=%s throws=%s ssl=%s", url, token, throws,
                  ssl_verify)

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
        if 'resource' in kwargs:
            del kwargs['resource']
        full_url = url if url else urljoin(self.url, path)
        full_url = full_url + ".json"
        headers = headers or {}
        params = params or {}
        if throws is None:
            throws = self._throws
        params.update(access_token=self._token)
        log.debug("[%s] (%s) params={%s} headers={%s} %s", method, full_url, params, headers,
                  kwargs if kwargs else '')
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

    @classmethod
    def _process_response(cls, response: requests.Response, throws=None) -> requests.Response:
        message = f"[RES] Response({response.status_code}): {response.content}"

        if response.ok:
            log.debug(message)
        else:
            log.error(message)
            if throws:
                raise errors.ApiClientError(response.status_code, response.reason, response.content)

        return response
