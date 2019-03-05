import logging
from typing import Dict

from threescale import utils
from threescale.defaults import DefaultClient, DefaultPlanResource, DefaultResource, \
    DefaultStateClient, DefaultUserResource

log = logging.getLogger(__name__)


class Services(DefaultClient):
    def __init__(self, *args, entity_name='service', entity_collection='services', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.threescale_client.admin_api_url + '/services'


class Metrics(DefaultClient):
    def __init__(self, *args, entity_name='metric', entity_collection='metrics', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.parent.url + '/metrics'


class Methods(DefaultClient):
    def __init__(self, *args, entity_name='method', entity_collection='methods', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.parent.url + '/methods'


class ApplicationPlans(DefaultClient):
    def __init__(self, *args, entity_name='application_plan', entity_collection='plans', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.parent.url + '/application_plans'


class Accounts(DefaultStateClient):
    def __init__(self, *args, entity_name='account', entity_collection='accounts', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
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

    def approve(self, entity_id, **kwargs):
        return self.set_state(entity_id=entity_id, state='approve', **kwargs)

    def reject(self, entity_id, **kwargs):
        return self.set_state(entity_id=entity_id, state='reject', **kwargs)

    def pending(self, entity_id, **kwargs):
        return self.set_state(entity_id=entity_id, state='make_pending', **kwargs)


class Applications(DefaultClient):
    def __init__(self, *args, entity_name='application', entity_collection='applications',
                 **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.parent.url + '/applications'


class Providers(DefaultClient):
    def __init__(self, *args, entity_name='user', entity_collection='users', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.threescale_client.admin_api_url + '/providers'


class ActiveDocs(DefaultClient):
    def __init__(self, *args, entity_name='active_doc', entity_collection='active_docs', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.threescale_client.admin_api_url + '/active_docs'


class Tenants(DefaultClient):
    def __init__(self, *args, entity_name='tenant', entity_collection='tenants', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.threescale_client.admin_api_url + '/tenants'


class Proxies(DefaultClient):
    def __init__(self, *args, entity_name='proxy', entity_collection='proxies', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)


# Resources

class ApplicationPlan(DefaultPlanResource):
    pass


class Method(DefaultResource):
    pass


class Metric(DefaultResource):
    @property
    def methods(self) -> Methods:
        return Methods(parent=self, instance_klass=Method)


class Proxy(DefaultResource):
    pass


class Service(DefaultResource):
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
    pass


class Provider(DefaultResource):
    pass


class Tenant(DefaultResource):
    pass


class Application(DefaultResource):
    pass


class Account(DefaultResource):
    @property
    def applications(self) -> Applications:
        return Applications(parent=self, instance_klass=Application)


class AccountUser(DefaultUserResource):
    @property
    def account(self) -> 'Account':
        return self.parent
