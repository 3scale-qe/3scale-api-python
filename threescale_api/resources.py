import logging
from typing import Dict, Union, List

import requests

from threescale_api import auth
from threescale_api import utils
from threescale_api import errors
from threescale_api.defaults import DefaultClient, DefaultPlanClient, DefaultPlanResource, \
    DefaultResource, DefaultStateClient, DefaultUserResource, DefaultStateResource

log = logging.getLogger(__name__)


class Services(DefaultClient):
    def __init__(self, *args, entity_name='service', entity_collection='services', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/services'


class MappingRules(DefaultClient):
    def __init__(self, *args, entity_name='mapping_rule', entity_collection='mapping_rules',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/mapping_rules'


class Metrics(DefaultClient):
    def __init__(self, *args, entity_name='metric', entity_collection='metrics', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/metrics'


class Limits(DefaultClient):
    def __init__(self, *args, entity_name='limit', entity_collection='limits', metric=None,
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        self._metric = metric

    @property
    def metric(self) -> Union['Metric', 'BackendMetric']:
        return self._metric

    @property
    def application_plan(self) -> 'ApplicationPlan':
        return self.parent

    def __call__(self, metric: 'Metric' = None) -> 'Limits':
        self._metric = metric
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


class PricingRules(DefaultClient):
    def __init__(self, *args, entity_name='pricing_rule', entity_collection='pricing_rules',
                 metric: 'Metric' = None, **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        self._metric = metric

    @property
    def metric(self) -> 'Metric':
        return self._metric

    @property
    def application_plan(self) -> 'ApplicationPlan':
        return self.parent

    def __call__(self, metric: 'Metric' = None) -> 'PricingRules':
        self._metric = metric
        return self

    @property
    def url(self) -> str:
        return self.application_plan.plans_url + f'/metrics/{self.metric.entity_id}/pricing_rules'


class Methods(DefaultClient):
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


class ApplicationPlanFeatures(DefaultClient):
    def __init__(self, *args, entity_name='feature', entity_collection='features', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/features'


class AccountUsers(DefaultClient):
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


class DevPortalAuthenticationProvider(DefaultClient):
    def __init__(self, *args, entity_name='authentication_provider',
                 entity_collection='authentication_providers', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/authentication_providers'


class ApplicationReferrerFilters(DefaultClient):
    def __init__(self, *args, entity_name='application', entity_collection='applications',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/referrer_filters'


class ApplicationKeys(DefaultClient):
    def __init__(self, *args, entity_name='application', entity_collection='applications',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/keys'


class Providers(DefaultClient):
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


class ActiveDocs(DefaultClient):
    def __init__(self, *args, entity_name='api_doc', entity_collection='api_docs', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/active_docs'


class Analytics(DefaultClient):
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

    def list_by_backend(self, backend: Union['Backend', int], **kwargs):
        backend_id = _extract_entity_id(backend)
        return self._list_by_resource(
            resource_id=backend_id, resource_type='backend_apis', **kwargs)


class Tenants(DefaultClient):
    def __init__(self, *args, entity_name='tenant', entity_collection='tenants', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.master_api_url + '/providers'


class Proxies(DefaultClient):
    def __init__(self, *args, entity_name='proxy', **kwargs):
        super().__init__(*args, entity_name=entity_name, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/proxy'

    def deploy(self) -> 'Proxy':
        log.info(f"[DEPLOY] {self._entity_name} to Staging")
        url = f'{self.url}/deploy'
        response = self.rest.post(url)
        instance = self._create_instance(response=response)
        return instance

    @property
    def oidc(self) -> 'OIDCConfigs':
        return OIDCConfigs(self)

    @property
    def mapping_rules(self) -> 'MappingRules':
        return MappingRules(parent=self, instance_klass=MappingRule)


class ProxyConfigs(DefaultClient):
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

    def latest(self, env: str = "sandbox") -> 'ProxyConfig':
        log.info(f"[LATEST] Get latest proxy configuration of {env}")
        self._env = env
        url = self.url + '/latest'
        response = self.rest.get(url=url)
        instance = self._create_instance(response=response)
        return instance

    def version(self, version: int = 1, env: str = "sandbox") -> 'ProxyConfig':
        log.info(f"[VERSION] Get proxy configuration of {env} of version {version}")
        self._env = env
        url = f'{self.url}/{version}'
        response = self.rest.get(url=url)
        instance = self._create_instance(response=response)
        return instance


class SettingsClient(DefaultClient):
    def __init__(self, *args, entity_name='settings', **kwargs):
        super().__init__(*args, entity_name=entity_name, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/settings'


class AdminPortalAuthenticationProvider(DefaultClient):
    def __init__(self, *args, entity_name='authentication_provider',
                 entity_collection='authentication_providers', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/account/authentication_providers'


class UserPermissionsClient(DefaultClient):
    def __init__(self, *args, entity_name='permissions', **kwargs):
        super().__init__(*args, entity_name=entity_name, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/tenants'


class Policies(DefaultClient):
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


class OIDCConfigs(DefaultClient):
    @property
    def url(self) -> str:
        return self.parent.url + '/oidc_configuration'

    def update(self, params: dict = None, **kwargs) -> dict:
        return self.rest.patch(url=self.url, json=params, **kwargs).json()

    def read(self, params: dict = None, **kwargs) -> dict:
        return self.rest.get(url=self.url, json=params, **kwargs).json()


class Backends(DefaultClient):
    def __init__(self, *args, entity_name='backend_api',
                 entity_collection='backend_apis', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/backend_apis'

    def list(self, **kwargs):
        return list(super().list(**kwargs))

    def _list(self, **kwargs):
        if "page" in kwargs.get("params", {}):
            return super()._list(**kwargs)

        pagenum = 1

        kwargs = kwargs.copy()
        if "params" not in kwargs:
            kwargs["params"] = {}

        kwargs["params"]["page"] = pagenum
        kwargs["params"]["per_page"] = 500

        page = super()._list(**kwargs)

        while len(page):
            for i in page:
                yield i
            pagenum += 1
            kwargs["params"]["page"] = pagenum
            page = super()._list(**kwargs)

    def __iter__(self):
        return self._list()


class BackendMetrics(Metrics):
    def __init__(self, *args, entity_name='metric', entity_collection='metrics', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)


class BackendMappingRules(MappingRules):
    def __init__(self, *args, entity_name='mapping_rule',
                 entity_collection='mapping_rules', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)


class BackendUsages(Services):
    def __init__(self, *args, entity_name='backend_usage',
                 entity_collection='backend_usages', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/backend_usages'


class PoliciesRegistry(DefaultClient):
    def __init__(self, *args, entity_name='policy', entity_collection='policies', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/registry/policies'


class ProviderAccounts(DefaultStateClient):
    """
    Client for Provider Accounts.
    In 3scale, entity under Account Settings > Users
    """

    def __init__(self, *args, entity_name='user', entity_collection='users', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/users'

    def permissions_update(self, entity_id: int,
                           allowed_services: [] = None, allowed_sections: [] = None, **kwargs):
        allowed_services = allowed_services if allowed_services else ['[]']
        allowed_sections = allowed_sections if allowed_sections else ['[]']

        log.info(self._log_message("Change of Provider Account (User) permissions"))
        url = self._entity_url(entity_id) + '/permissions'
        params = {
            'allowed_service_ids[]': allowed_services,
            'allowed_sections[]': allowed_sections,
        }
        response = self.rest.put(url=url, data=params, **kwargs)
        return response.json()

    def allow_all_sections(self, entity_id: int, **kwargs):
        log.info(self._log_message("Change of Provider Account (User) "
                                   "permissions to all available permissions"))
        return self.permissions_update(entity_id=entity_id, allowed_sections=[
            'portal', 'finance', 'settings', 'partners', 'monitoring', 'plans', 'policy_registry'
        ])

    def permissions_read(self, entity_id: int, **kwargs):
        url = self._entity_url(entity_id) + '/permissions'
        response = self.rest.get(url=url, **kwargs)
        return response.json()

    def set_role_member(self, entity_id: int):
        log.info("Changes the role of the user of the provider account to member")
        return self.set_state(entity_id, state='member')

    def set_role_admin(self, entity_id: int):
        log.info("Changes the role of the provider account to admin")
        return self.set_state(entity_id, state='admin')

    def suspend(self, entity_id):
        log.info("Changes the state of the user of the provider account to suspended")
        return self.set_state(entity_id, state='suspend')

    def unsuspend(self, entity_id: int):
        log.info("Revokes the suspension of a user of the provider account")
        return self.set_state(entity_id, state='unsuspend')

    def activate(self, entity_id: int):
        log.info("Changes the state of the user of the provider account to active")
        return self.set_state(entity_id, state='activate')


class Webhooks(DefaultClient):
    """
    Default client for webhooks
    """

    def __init__(self, *args, entity_name='webhook', entity_collection='webhooks', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/webhooks'

    def update(self, params: dict = None, **kwargs):
        url = self.url
        return self.rest.put(url=url, json=params, **kwargs)

    def setup(self, webhook_type, url):
        """
        Configure webhooks for given webhooks type
        """
        params = {"url": url,
                  "active": "true",
                  "provider_actions": "true"}
        if webhook_type == "Keys":
            params.update({
                "application_key_created_on": "true",
                "application_key_deleted_on": "true",
                "application_key_updated_on": "true"
            })
        elif webhook_type == "Users":
            params.update({
                "user_created_on": "true",
                "user_updated_on": "true",
                "user_deleted_on": "true"
            })
        elif webhook_type == "Applications":
            params.update({
                "application_created_on": "true",
                "application_updated_on": "true",
                "application_suspended_on": "true",
                "application_plan_changed_on": "true",
                "application_user_key_updated_on": "true",
                "application_deleted_on": "true"
            })
        elif webhook_type == "Accounts":
            params.update({
                "account_created_on": "true",
                "account_updated_on": "true",
                "account_deleted_on": "true",
                "account_plan_changed_on": "true"
            })

        return self.update(params=params)

    def clear(self):
        """
        Configure webhooks to default settings
        """
        params = {"url": "",
                  "active": "false",
                  "provider_actions": "false",
                  "account_created_on": "false",
                  "account_updated_on": "false",
                  "account_deleted_on": "false",
                  "user_created_on": "false",
                  "user_updated_on": "false",
                  "user_deleted_on": "false",
                  "application_created_on": "false",
                  "application_updated_on": "false",
                  "application_deleted_on": "false",
                  "account_plan_changed_on": "false",
                  "application_plan_changed_on": "false",
                  "application_user_key_updated_on": "false",
                  "application_key_created_on": "false",
                  "application_key_deleted_on": "false",
                  "application_suspended_on": "false",
                  "application_key_updated_on": "false",
                  }
        return self.update(params=params)


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


class Method(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def metric(self) -> 'Metric':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.metric.parent


class Metric(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def methods(self) -> 'Methods':
        return Methods(parent=self, instance_klass=Method)


class MappingRule(DefaultResource):
    @property
    def proxy(self) -> 'Proxy':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.proxy.service


class ProxyConfig(DefaultResource):
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

    # Same problem as in __getitem__.
    def __len__(self):
        if "proxy_configs" in self.entity:
            return len(self.entity["proxy_configs"])
        else:
            return super().__len__()


class Policy(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def proxy(self) -> 'Proxy':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.proxy.service


class Proxy(DefaultResource):
    @property
    def url(self) -> str:
        return self.client.url

    @property
    def service(self) -> 'Service':
        return self.parent

    @property
    def mapping_rules(self) -> MappingRules:
        return MappingRules(parent=self, instance_klass=MappingRule)

    @property
    def configs(self) -> 'ProxyConfigs':
        return ProxyConfigs(parent=self, instance_klass=ProxyConfig)

    @property
    def policies(self) -> 'Policies':
        return Policies(parent=self, instance_klass=Policy)

    @property
    def entity_id(self):
        return None

    def promote(self, **kwargs) -> 'Proxy':
        return self.configs.promote(**kwargs)

    @property
    def policies_registry(self) -> PoliciesRegistry:
        return PoliciesRegistry(parent=self, instance_klass=PolicyRegistry)

    def deploy(self) -> 'Proxy':
        return self.client.deploy()


class Service(DefaultResource):
    AUTH_USER_KEY = "1"
    AUTH_APP_ID_KEY = "2"
    AUTH_OIDC = "oidc"

    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def app_plans(self) -> ApplicationPlans:
        return ApplicationPlans(parent=self, instance_klass=ApplicationPlan)

    @property
    def metrics(self) -> Metrics:
        return Metrics(parent=self, instance_klass=Metric)

    @property
    def proxy(self) -> 'Proxies':
        return Proxies(parent=self, instance_klass=Proxy)

    @property
    def mapping_rules(self) -> 'MappingRules':
        return self.proxy.mapping_rules

    @property
    def policies_registry(self) -> 'PoliciesRegistry':
        return PoliciesRegistry(parent=self, instance_klass=PoliciesRegistry)

    def oidc(self):
        return self.proxy.oidc

    @property
    def backend_usages(self) -> 'BackendUsages':
        return BackendUsages(parent=self, instance_klass=BackendUsage)

    @property
    def active_docs(self) -> 'ActiveDocs':
        """ Active docs related to service. """
        up_self = self

        class Wrap(ActiveDocs):
            def list(self, **kwargs) -> List['DefaultResource']:
                """List all ActiveDocs related to this service."""
                kwargs.update({'service_id': up_self['id']})
                instance = self.select_by(**kwargs)
                return instance

        return Wrap(parent=self, instance_klass=ActiveDoc)


class ActiveDoc(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Provider(DefaultResource):
    def __init__(self, entity_name='org_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Tenant(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def entity_id(self) -> int:
        return self.entity["signup"]["account"]["id"]


class Application(DefaultResource):
    def __init__(self, entity_name='name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)
        self._auth_objects = {
            Service.AUTH_USER_KEY: auth.UserKeyAuth,
            Service.AUTH_APP_ID_KEY: auth.AppIdKeyAuth
        }
        self._api_client_verify = None
        self._client_factory = utils.HttpClient

    @property
    def account(self) -> 'Account':
        return self.parent

    @property
    def service(self) -> 'Service':
        "The service to which this application is bound"
        return self.threescale_client.services[self["service_id"]]

    @property
    def keys(self):
        "Application keys"
        return ApplicationKeys(parent=self, instance_klass=DefaultResource)

    @property
    def authobj(self) -> requests.auth.AuthBase:
        """Returns subclass of requests.auth.BaseAuth to provide authentication
        for queries agains 3scale service"""

        svc = self.service
        auth_mode = svc["backend_version"]

        if auth_mode not in self._auth_objects:
            raise errors.ThreeScaleApiError(f"Unknown credentials for configuration {auth_mode}")

        return self._auth_objects[auth_mode](self)

    def register_auth(self, auth_mode: str, factory):
        self._auth_objects[auth_mode] = factory

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

        return self._client_factory(self, endpoint, session, verify)

    @property
    def api_client_verify(self) -> bool:
        """Allows to change defaults of SSL verification for api_client (and
        test_request); default: None - do not alter library default"""

        return self._api_client_verify

    @api_client_verify.setter
    def api_client_verify(self, value: bool):
        self._api_client_verify = value

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


class Account(DefaultResource):
    def __init__(self, entity_name='org_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def applications(self) -> Applications:
        return Applications(parent=self, instance_klass=Application)

    @property
    def users(self) -> AccountUsers:
        return AccountUsers(parent=self, instance_klass=AccountUser)


class UserPermissions(DefaultResource):
    pass


class AccountUser(DefaultUserResource):
    def __init__(self, entity_name='username', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def account(self) -> 'Account':
        return self.parent

    @property
    def permissions(self) -> 'UserPermissionsClient':
        return UserPermissionsClient(parent=self, instance_klass=UserPermissions)


class AccountPlan(DefaultResource):
    def __init__(self, entity_name='name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Limit(DefaultResource):
    @property
    def app_plan(self) -> ApplicationPlan:
        return self.parent


class PricingRule(DefaultResource):
    @property
    def app_plan(self) -> ApplicationPlan:
        return self.parent


class Backend(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def metrics(self) -> 'BackendMetrics':
        return BackendMetrics(parent=self, instance_klass=BackendMetric)

    @property
    def mapping_rules(self) -> 'BackendMappingRules':
        return BackendMappingRules(parent=self, instance_klass=BackendMappingRule)

    @property
    def usages(self) -> 'BackendUsages':
        return BackendUsages(parent=self, instance_klass=BackendUsages)


class BackendMetric(Metric):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class BackendMappingRule(MappingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BackendUsage(DefaultResource):
    def __init__(self, entity_name='', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def backend(self) -> 'Backend':
        return Backend(
            client=Backends(parent=self, instance_klass=Backend),
            entity_id=self['backend_id'])


def _extract_entity_id(entity: Union['DefaultResource', int]):
    if isinstance(entity, DefaultResource):
        return entity.entity_id
    return entity


class PolicyRegistry(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def proxy(self) -> 'Proxy':
        return self.parent

    @property
    def service(self) -> 'Service':
        return self.proxy.service


class ProviderAccount(DefaultStateResource):
    def __init__(self, entity_name='username', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    def permissions_update(
            self, allowed_services: [] = None, allowed_sections: [] = None, **kwargs):
        return self.client.permissions_update(
            entity_id=self.entity_id,
            allowed_services=allowed_services,
            allowed_sections=allowed_sections,
            **kwargs
        )

    def allow_all_sections(self, **kwargs):
        return self.client.allow_all_sections(entity_id=self.entity_id, **kwargs)

    def permissions_read(self, **kwargs):
        return self.client.permissions_read(entity_id=self.entity_id, **kwargs)

    def set_role_member(self):
        log.info("Changes the role of the user of the provider account to member")
        return self.set_state(state='member')

    def set_role_admin(self):
        log.info("Changes the role of the provider account to admin")
        return self.set_state(state='admin')

    def suspend(self):
        log.info("Changes the state of the user of the provider account to suspended")
        return self.set_state(state='suspend')

    def unsuspend(self):
        log.info("Revokes the suspension of a user of the provider account")
        return self.set_state(state='unsuspend')

    def activate(self):
        log.info("Changes the state of the user of the provider account to active")
        return self.set_state(state='activate')
