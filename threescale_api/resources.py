import logging
from typing import Dict, Union

from threescale_api import utils
from threescale_api.defaults import DefaultClient, DefaultPlanClient, DefaultPlanResource, \
    DefaultResource, DefaultStateClient, DefaultUserResource

log = logging.getLogger(__name__)


class Services(DefaultClient):
    def __init__(self, *args, entity_name='service', entity_collection='services', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/services'


class MappingRules(DefaultClient):
    def __init__(self, *args, entity_name='mapping_rule', entity_collection='mapping_rules', **kwargs):
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
    def metric(self) -> 'Metric':
        return self._metric

    def __call__(self, metric: 'Metric' = None) -> 'Limits':
        self._metric = metric
        return self

    @property
    def url(self) -> str:
        return self.parent.url + f'/metrics/{self.metric.entity_id}/limits'

    def list_per_app_plan(self, **kwargs):
        log.info(f"[LIST] List limits per app plan: {kwargs}")
        url = self.parent.url + '/limits'
        response = self.rest.get(url=url, **kwargs)
        instance = self._create_instance(response=response)
        return instance


class PricingRules(DefaultClient):
    def __init__(self, *args, entity_name='rule', entity_collection='rules', metric=None, **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)
        self._metric = metric

    @property
    def metric(self) -> 'Metric':
        return self._metric

    def __call__(self, metric: 'Metric' = None) -> 'PricingRules':
        self._metric = metric
        return self

    @property
    def url(self) -> str:
        return self.parent.url + f'/metrics/{self.metric.entity_id}/pricing_rules'


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


class Tenants(DefaultClient):
    def __init__(self, *args, entity_name='tenant', entity_collection='tenants', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url + '/tenants'


class Proxies(DefaultClient):
    def __init__(self, *args, entity_name='proxy', **kwargs):
        super().__init__(*args, entity_name=entity_name,  **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/proxy'


class ProxyConfigs(DefaultClient):
    def __init__(self, *args, entity_name='config', entity_collection='configs', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self) -> str:
        return self.parent.url + '/configs'


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


# Resources

class ApplicationPlan(DefaultPlanResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def service(self) -> 'Service':
        return self.parent


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
    def methods(self) -> Methods:
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
    def url(self):
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


class Service(DefaultResource):
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


class ActiveDoc(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Provider(DefaultResource):
    def __init__(self, entity_name='org_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Tenant(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


class Application(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    @property
    def account(self) -> 'Account':
        return self.parent


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
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)


def _extract_entity_id(entity: Union['DefaultResource', int]):
    if isinstance(entity, DefaultResource):
        return entity.entity_id
    return entity
