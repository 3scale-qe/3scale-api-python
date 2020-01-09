import logging
import functools
from typing import Dict, Union

import requests

from threescale_api import auth
from threescale_api import utils
from threescale_api import errors
from threescale_api.defaults import CRUDClient, DefaultPlanClient, DefaultPlanResource, \
    CRUDResource, DefaultStateClient, DefaultUserResource

log = logging.getLogger(__name__)


class Services(CRUDClient):
    def __init__(self, *args, entity_name='service', entity_collection='services', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/services'


class MappingRules(CRUDClient):
    def __init__(self, *args, entity_name='mapping_rule', entity_collection='mapping_rules',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/mapping_rules'


class Metrics(CRUDClient):
    def __init__(self, *args, entity_name='metric', entity_collection='metrics', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/metrics'


class Limits(CRUDClient):
    def __init__(self, *args, entity_name='limit', entity_collection='limits', metric=None,
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        self.__metric = metric

    @property
    def metric(self) -> 'Metric':
        return self.__metric

    @property
    def application_plan(self) -> 'ApplicationPlan':
        return self.parent

    def __call__(self, metric: 'Metric' = None) -> 'Limits':
        self.__metric = metric
        return self

    @property
    def url(self) -> str:
        return self.application_plan.plans_url + f'/metrics/{self.metric.entity_id}/limits'

    def list_per_app_plan(self, **kwargs):
        log.info(f"[LIST] List limits per app plan: {kwargs}")
        url = self.parent.url + '/limits'
        response = self.rest.get(url=url, **kwargs)
        instance = self._create_instance(response=response)
        return instance


class PricingRules(CRUDClient):
    def __init__(self, *args, entity_name='pricing_rule', entity_collection='pricing_rules',
                 metric: 'Metric' = None, **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        self.__metric = metric

    @property
    def metric(self) -> 'Metric':
        return self.__metric

    @property
    def application_plan(self) -> 'ApplicationPlan':
        return self.parent

    def __call__(self, metric: 'Metric' = None) -> 'PricingRules':
        self.__metric = metric
        return self

    @property
    def url(self) -> str:
        return self.application_plan.plans_url + f'/metrics/{self.metric.entity_id}/pricing_rules'


class Methods(CRUDClient):
    def __init__(self, *args, entity_name='method', entity_collection='methods', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/methods'


class ApplicationPlans(DefaultPlanClient):
    def __init__(self, *args, entity_name='application_plan', entity_collection='plans', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/application_plans'

    @property
    def plans_url(self) -> str:
        return self.threescale_client.admin_api_url + '/application_plans'


class ApplicationPlanFeatures(CRUDClient):
    def __init__(self, *args, entity_name='feature', entity_collection='features', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/features'


class AccountUsers(CRUDClient):
    def __init__(self, *args, entity_name='user', entity_collection='users', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/users'


class AccountPlans(DefaultPlanClient):
    def __init__(self, *args, entity_name='account_plan', entity_collection='plans', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/account_plans'


class Accounts(DefaultStateClient):
    def __init__(self, *args, entity_name='account', entity_collection='accounts', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/accounts'

    def create(self, params: dict = None, **kwargs) -> 'Account':
        """Create new account
        Args:
            params(dict): Parameters to used to create new instance
            **kwargs: Optional args
        Returns(Account): Account instance
        """
        return self.signup(params=params, **kwargs)

    def signup(self, params: dict, **kwargs) -> 'Account':
        """Sign Up for an account
        Args:
            params(dict): Parameters to used to create new instance
            **kwargs: Optional args
        Returns(Account): Account instance
        """
        log.info(f"[SIGNUP] Create new Signup: {kwargs}")
        url = self.threescale_client.admin_api_url + '/signup'
        response = self.rest.post(url=url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance

    def set_plan(self, entity_id: int, plan_id: int, **kwargs):
        """Sets account plan for the account
        Args:
            entity_id: Entity id
            plan_id: Plan id
            **kwargs: Optional args
        Returns:
        """
        log.info(f"[PLAN] Set plan for an account({entity_id}): {plan_id}")
        params = dict(plan_id=plan_id)
        url = self._entity_url(entity_id=entity_id) + '/change_plan'
        response = self.rest.put(url=url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance

    def send_message(self, entity_id: int, body: str, **kwargs) -> Dict:
        """Send message to a developer account
        Args:
            entity_id(int): Entity id
            body(str): Message body
            **kwargs: Optional args
        Returns(Dict): Response
        """
        log.info(f"[MSG] Send message to account ({entity_id}): {body} {kwargs}")
        params = dict(body=body)
        url = self._entity_url(entity_id=entity_id) + '/messages'
        response = self.rest.post(url=url, json=params, **kwargs)
        instance = utils.extract_response(response=response)
        return instance

    def approve(self, entity_id: int, **kwargs) -> 'Account':
        """Approve the account
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args
        Returns(Account): Account resource
        """
        return self.set_state(entity_id=entity_id, state='approve', **kwargs)

    def reject(self, entity_id, **kwargs) -> 'Account':
        """Reject the account
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args
        Returns(Account): Account resource
        """
        return self.set_state(entity_id=entity_id, state='reject', **kwargs)

    def pending(self, entity_id, **kwargs) -> 'Account':
        """Set the account as pending
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args
        Returns(Account): Account resource
        """
        return self.set_state(entity_id=entity_id, state='make_pending', **kwargs)


class Applications(DefaultStateClient):
    def __init__(self, *args, entity_name='application', entity_collection='applications',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/applications'

    def change_plan(self, entity_id: int, plan_id: int, **kwargs):
        log.info(f"[PLAN] Change plan for application ({entity_id}) to {plan_id} {kwargs}")
        params = dict(plan_id=plan_id)
        url = self._entity_url(entity_id=entity_id) + '/change_plan'
        response = self.rest.put(url=url, json=params, **kwargs)
        instance = utils.extract_response(response=response)
        return instance

    def customize_plan(self, entity_id: int, **kwargs):
        log.info(f"[PLAN] Customize plan for application ({entity_id}) {kwargs}")
        url = self._entity_url(entity_id=entity_id) + '/customize_plan'
        response = self.rest.put(url=url, **kwargs)
        instance = utils.extract_response(response=response)
        return instance

    def decustomize_plan(self, entity_id: int, **kwargs):
        log.info(f"[PLAN] Decustomize plan for application ({entity_id}) {kwargs}")
        url = self._entity_url(entity_id=entity_id) + '/decustomize_plan'
        response = self.rest.put(url=url, **kwargs)
        instance = utils.extract_response(response=response)
        return instance

    def accept(self, entity_id: int, **kwargs):
        self.set_state(entity_id=entity_id, state='accept', **kwargs)

    def suspend(self, entity_id: int, **kwargs):
        self.set_state(entity_id=entity_id, state='suspend', **kwargs)

    def resume(self, entity_id: int, **kwargs):
        self.set_state(entity_id=entity_id, state='resume', **kwargs)


class DevPortalAuthenticationProvider(CRUDClient):
    def __init__(self, *args, entity_name='authentication_provider',
                 entity_collection='authentication_providers', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/authentication_providers'


class ApplicationReferrerFilters(CRUDClient):
    def __init__(self, *args, entity_name='application', entity_collection='applications',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/referrer_filters'


class ApplicationKeys(CRUDClient):
    def __init__(self, *args, entity_name='application', entity_collection='applications',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/keys'


class Providers(CRUDClient):
    def __init__(self, *args, entity_name='user', entity_collection='users', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/providers'

    def create_token(self, entity_id: int, params, **kwargs):
        log.info(self._log_message("[TOKEN] Create token",
                                   entity_id=entity_id, body=params, **kwargs))
        url = self._entity_url(entity_id=entity_id) + '/access_tokens'
        response = self.rest.put(url, json=params)
        return utils.extract_response(response=response)


class ActiveDocs(CRUDClient):
    def __init__(self, *args, entity_name='api_doc', entity_collection='api_docs', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/active_docs'


class Analytics(CRUDClient):
    def _list_by_resource(self, resource_id: int, resource_type, metric_name: str = 'hits',
                          since=None, period: str = 'year', **kwargs):
        log.info(f"List analytics by {resource_type} ({resource_id}) f"
                 f"or metric (#{metric_name})")
        params = dict(
            metric_name=metric_name,
            since=since,
            period=period,
            **kwargs
        )
        url = self.threescale_client.url + f"/stats/{resource_type}/{resource_id}/usage"
        response = self.rest.get(url, json=params)
        return utils.extract_response(response=response)

    def list_by_application(self, application: Union['Application', int], **kwargs):
        app_id = _extract_entity_id(application)
        return self._list_by_resource(resource_id=app_id, resource_type='applications', **kwargs)

    def list_by_service(self, service: Union['Service', int], **kwargs):
        app_id = _extract_entity_id(service)
        return self._list_by_resource(resource_id=app_id, resource_type='services', **kwargs)


class Tenants(CRUDClient):
    def __init__(self, *args, entity_name='tenant', entity_collection='tenants', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/tenants'


class Proxies(CRUDClient):
    def __init__(self, *args, entity_name='proxy', **kwargs):
        super().__init__(*args, entity_name=entity_name, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/proxy'

    @property
    def oidc(self) -> 'OIDCConfigs':
        return OIDCConfigs(self)


class ProxyConfigs(CRUDClient):
    def __init__(self, *args, entity_name='proxy_config', entity_collection='configs',
                 env: str = None, **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        self._env = env

    @property
    def url(self) -> str:
        base = self.parent.url + '/configs'
        return base if not self._env else f"{base}/{self._env}"

    @property
    def proxy(self) -> 'Proxy':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.proxy.service

    # tests/integration/test_integration_services.py::test_service_list_configs
    # defines usage in a form proxy.configs.list(env='staging').
    # To reflect this (good tests are considered immutable and defining the behavior)
    # list method has to be customized
    def list(self, **kwargs):
        if "env" in kwargs:
            self._env = kwargs["env"]
            del (kwargs["env"])
        return super().list(**kwargs)

    def promote(self, version: int = 1, from_env: str = 'sandbox', to_env: str = 'production',
                **kwargs) -> 'Proxy':
        log.info(f"[PROMOTE] {self.service} version {version} from {from_env} to {to_env}")
        url = f'{self.url}/{from_env}/{version}/promote'
        params = dict(to=to_env)
        kwargs.update()
        response = self.rest.post(url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance


class SettingsClient(CRUDClient):
    def __init__(self, *args, entity_name='settings', **kwargs):
        super().__init__(*args, entity_name=entity_name, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/settings'


class AdminPortalAuthenticationProvider(CRUDClient):
    def __init__(self, *args, entity_name='authentication_provider',
                 entity_collection='authentication_providers', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/account/authentication_providers'


class UserPermissionsClient(CRUDClient):
    def __init__(self, *args, entity_name='permissions', **kwargs):
        super().__init__(*args, entity_name=entity_name, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/tenants'


class Policies(CRUDClient):
    def __init__(self, *args, entity_name='policy', entity_collection='policies', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return f"{self.parent.url}/{self._entity_collection}"

    def append(self, *policies):
        params = self.list().entity
        params["policies_config"].extend(policies)
        params["service_id"] = self.parent["service_id"]
        return self.update(params=params)

    def insert(self, index: int, *policies):
        params = self.list().entity
        for (i, policy) in enumerate(policies):
            params["policies_config"].insert(index + i, policy)
        params["service_id"] = self.parent["service_id"]
        return self.update(params=params)


class OIDCConfigs(CRUDClient):
    @property
    def url(self) -> str:
        return self.parent.url + '/oidc_configuration'

    def update(self, params: dict = None, **kwargs) -> 'CRUDResource':
        return self.rest.patch(url=self.url, json=params, **kwargs)


# Resources

class ApplicationPlan(DefaultPlanResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def plans_url(self) -> str:
        return self.threescale_client.admin_api_url + f"/application_plans/{self.entity_id}"

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def limits(self, metric: 'Metric' = None) -> 'Limits':
        return Limits(self, metric=metric, instance_klass=Limit)

    @property
    def pricing_rules(self, metric: 'Metric' = None) -> 'PricingRules':
        return PricingRules(self, metric=metric, instance_klass=PricingRule)


class Method(CRUDResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def metric(self) -> 'Metric':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.metric.parent


class Metric(CRUDResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)
        self.__methods = Methods(parent=self, instance_klass=Method)

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def methods(self) -> 'Methods':
        return self.__methods


class MappingRule(CRUDResource):
    @property
    def proxy(self) -> 'Proxy':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.proxy.service


class ProxyConfig(CRUDResource):
    @property
    def proxy(self) -> 'Proxy':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.proxy.service

    # ProxyConfig is once instantiated with just proxy config obj (for example
    # through promote()) other times as dict of key "proxy_configs". This seems
    # to be clear bug in the code (this code) and behavior should be always
    # consistent. For now keeping inconsistency as it introduces minimal change
    # and keeps everything working
    def __getitem__(self, key):
        if "proxy_configs" in self.entity:
            return self.entity["proxy_configs"][key]
        else:
            return super().__getitem__(key)


class Policy(CRUDResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def proxy(self) -> 'Proxy':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.proxy.service


class Proxy(CRUDResource):
    @property
    def url(self) -> str:
        return self.client.url

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    @functools.lru_cache()
    def mapping_rules(self) -> MappingRules:
        return MappingRules(parent=self, instance_klass=MappingRule)

    @property
    @functools.lru_cache()
    def configs(self) -> 'ProxyConfigs':
        return ProxyConfigs(parent=self, instance_klass=ProxyConfig)

    @property
    @functools.lru_cache()
    def policies(self) -> 'Policies':
        return Policies(parent=self, instance_klass=Policy)

    @property
    def entity_id(self) -> None:
        return None

    def promote(self, **kwargs) -> 'Proxy':
        return self.configs.promote(**kwargs)


class Service(CRUDResource):
    AUTH_USER_KEY = "1"
    AUTH_APP_ID_KEY = "2"
    AUTH_OIDC = "oidc"

    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)
        self.__app_plans = ApplicationPlans(parent=self, instance_klass=ApplicationPlan)
        self.__metrics = Metrics(parent=self, instance_klass=Metric)
        self.__proxies = Proxies(parent=self, instance_klass=Proxy)
        self.__mapping_rules = MappingRules(parent=self, instance_klass=MappingRule)

    @property
    def app_plans(self) -> ApplicationPlans:
        return self.__app_plans

    @property
    def metrics(self) -> Metrics:
        return self.__metrics

    @property
    def proxy(self) -> 'Proxies':
        return self.__proxies

    @property
    def mapping_rules(self) -> 'MappingRules':
        return self.__mapping_rules


class ActiveDoc(CRUDResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Provider(CRUDResource):
    def __init__(self, entity_name='org_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Tenant(CRUDResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Application(CRUDResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)
        self.__auth_objects = {
            Service.AUTH_USER_KEY: auth.UserKeyAuth,
            Service.AUTH_APP_ID_KEY: auth.AppIdKeyAuth
        }
        self.__api_client_verify = None

    @property
    def account(self) -> 'Account':
        return self.parent

    @property
    def service(self) -> 'Service':
        """The service to which this application is bound"""
        return self.threescale_client.services[self["service_id"]]

    @property
    def keys(self):
        """Application keys"""
        return ApplicationKeys(parent=self, instance_klass=CRUDResource)

    @property
    def authobj(self) -> requests.auth.AuthBase:
        """Returns subclass of requests.auth.BaseAuth to provide authentication
        for queries against 3scale service"""

        svc = self.service
        auth_mode = svc["backend_version"]

        if auth_mode not in self.__auth_objects:
            raise errors.ThreeScaleApiError(f"Unknown credentials for configuration {auth_mode}")

        return self.__auth_objects[auth_mode](self)

    def register_auth(self, auth_mode: str, factory):
        self.__auth_objects[auth_mode] = factory

    def api_client(self, endpoint: str = "sandbox_endpoint",
                   session: requests.Session = None, verify: bool = None) -> 'utils.HttpClient':
        """This is preconfigured client for the application to run api calls.
        To avoid failures due to delays in infrastructure it retries call
        in case of certain condition. To modify this behavior customized session
        has to be passed. This custom session should have configured all necessary
        (e.g. authentication)

        :param endpoint: Choose whether 'sandbox_endpoint' or 'endpoint',
                defaults to sandbox_endpoint
        :param session: Customized requests.Session, all necessary has to be already done
        :param verify: Whether to do ssl verification or not,
                by default doesn't change what's in session, defaults to None

        :return: threescale.utils.HttpClient

        Instance property api_client_verify of Application can change default of verify param
        to avoid passing non-default value to multiple api_client calls. It is applied whenever
        verify param is kept unchanged (None).
        """

        if verify is None:
            verify = self.api_client_verify

        return utils.HttpClient(self, endpoint, session, verify)

    @property
    def api_client_verify(self) -> bool:
        """Allows to change defaults of SSL verification for api_client (and
        test_request); default: None - do not alter library default"""

        return self.__api_client_verify

    @api_client_verify.setter
    def api_client_verify(self, value: bool):
        self.__api_client_verify = value

    def test_request(self, relpath=None, verify: bool = None):
        """Quick call to do test request against configured service. This is
        equivalent to test request on Integration page from UI

        :param relpath: relative path to run the requests,
                if not set, preconfigured value is used, defaults to None
        :param verify: SSL verification

        :return: requests.Response

        Instance attribute api_client_verify of Application can change default of verify param
        to avoid passing non-default value to multiple test_request calls.
        """
        proxy = self.service.proxy.list().entity
        relpath = relpath if relpath is not None else proxy["api_test_path"]
        client = self.api_client(verify=verify)

        return client.get(relpath)


class Account(CRUDResource):
    def __init__(self, entity_name='org_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)
        self.__apps = Applications(parent=self, instance_klass=Application)
        self.__users = AccountUsers(parent=self, instance_klass=AccountUser)

    @property
    def applications(self) -> Applications:
        return self.__apps

    @property
    def users(self) -> AccountUsers:
        return self.__users


class UserPermissions(CRUDResource):
    pass


class AccountUser(DefaultUserResource):
    def __init__(self, entity_name='username', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)
        self.__permissions = UserPermissionsClient(parent=self, instance_klass=UserPermissions)

    @property
    def account(self) -> 'Account':
        return self.parent

    @property
    def permissions(self) -> 'UserPermissionsClient':
        return self.__permissions


class AccountPlan(CRUDResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Limit(CRUDResource):
    @property
    def app_plan(self) -> ApplicationPlan:
        return self.parent


class PricingRule(CRUDResource):
    @property
    def app_plan(self) -> ApplicationPlan:
        return self.parent


def _extract_entity_id(entity: Union['CRUDResource', int]):
    if isinstance(entity, CRUDResource):
        return entity.entity_id
    return entity
