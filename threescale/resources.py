import logging
from typing import List, TYPE_CHECKING

import requests

from threescale import utils

if TYPE_CHECKING:
    from .client import TheeScaleClient, RestApiClient

log = logging.getLogger(__name__)


class DefaultClient:
    def __init__(self, parent=None, instance_klass=None, entity_name=None, entity_collection=None):
        self._parent = parent
        self._instance_klass = instance_klass
        self._entity_name = entity_name
        if entity_collection is None and entity_name is not None:
            entity_collection = f'{entity_name}s'
        self._entity_collection = entity_collection

    @property
    def url(self) -> str:
        return self.threescale_client.admin_api_url

    @property
    def threescale_client(self) -> 'TheeScaleClient':
        return self.parent.threescale_client

    @property
    def parent(self) -> 'DefaultClient':
        return self._parent

    @property
    def rest(self) -> 'RestApiClient':
        return self.threescale_client.rest

    def list(self, **kwargs) -> List['DefaultResource']:
        """List all entities
        Args:
            **kwargs: Params
        Returns(List['DefaultResource]): List of resources
        """
        log.info(f"[LIST] List {self._instance_klass.__name__}: {kwargs}")
        url = self._entity_url()
        response = self.rest.get(url=url, **kwargs)
        instance = self._create_instance(response=response, collection=True)
        return instance

    def create(self, params: dict = None, **kwargs) -> 'DefaultResource':
        """Create a new instance
        Args:
            params: Parameters required to create new instance
            **kwargs:

        Returns:

        """
        log.info(f"[CREATE] Create new {self._instance_klass.__name__}: {kwargs}")
        url = self._entity_url()
        response = self.rest.post(url=url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance

    def delete(self, entity_id=None, **kwargs) -> bool:
        log.info(f"[DELETE] Delete {self._instance_klass.__name__}({entity_id}): {kwargs}")
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.delete(url=url, **kwargs)
        return response.ok

    def exists(self, entity_id=None, **kwargs) -> bool:
        log.debug(f"[EXIST] Resource exist {self._instance_klass.__name__}({entity_id})): {kwargs}")
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.get(url=url, throws=False, **kwargs)
        return response.ok

    def update(self, entity_id=None, params: dict = None, **kwargs) -> 'DefaultResource':
        log.info(f"[UPDATE] Update {self._instance_klass.__name__}({entity_id}): {kwargs}")
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.put(url=url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance

    def fetch(self, entity_id: int = None, **kwargs) -> dict:
        log.debug(f"[FETCH] Fetch {self._instance_klass.__name__}({entity_id})")
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.get(url=url, **kwargs)
        return utils.extract_response(response=response)

    def read(self, entity_id: int = None) -> 'DefaultResource':
        log.debug(f"[READ] Read {self._instance_klass.__name__}({entity_id})")
        return self._instance_klass(client=self, entity_id=entity_id)

    def _entity_url(self, entity_id=None) -> str:
        if not entity_id:
            return self.url
        return self.url + '/' + str(entity_id)

    def _create_instance(self, response: requests.Response, klass=None, collection: bool = False):
        klass = klass or self._instance_klass
        extract_params = dict(response=response, entity=self._entity_name)
        if collection:
            extract_params['collection'] = self._entity_collection
        extracted = utils.extract_response(**extract_params)
        if collection and isinstance(extracted, list):
            instances = [self.__make_instance(item, klass) for item in extracted]
            log.debug(f"[INSTANCE] Created instances: {instances}")
            return instances
        instance = self.__make_instance(extracted, klass)
        log.debug(f"[INSTANCE] Created instance: {instance}")
        return instance

    def __make_instance(self, extracted: dict, klass):
        instance = klass(client=self, entity=extracted) if klass else extracted
        return instance


class DefaultResource:
    def __init__(self, client: DefaultClient = None, entity_id: int = None, entity: dict = None):
        self._entity_id = entity_id
        self._entity = entity
        self._client = client

    @property
    def url(self) -> str:
        return self.client.url + f"/{self.entity_id}"

    @property
    def entity(self) -> dict:
        self._lazy_load()
        return self._entity

    @property
    def client(self) -> DefaultClient:
        return self._client

    @property
    def entity_id(self) -> int:
        return self._entity_id or self._entity.get('id')

    def __getitem__(self, item: str):
        return self.get(item)

    def __setitem__(self, key: str, value):
        self.set(key, value)

    def __str__(self) -> str:
        return self.__class__.__name__ + f"({self.entity_id}): " + str(self.entity)

    def __repr__(self) -> str:
        return str(self)

    def get(self, item):
        return self.entity.get(item)

    def set(self, item, value):
        self.entity[item] = value

    def _lazy_load(self, **kwargs) -> 'DefaultResource':
        if not self._entity:
            # Lazy load the entity
            self._entity = self._client.fetch(self.entity_id, **kwargs)
        return self

    def read(self, **kwargs) -> 'DefaultResource':
        self._invalidate()
        self._lazy_load(**kwargs)
        return self

    def exists(self, **kwargs) -> bool:
        return self.client.exists(entity_id=self.entity_id, **kwargs)

    def delete(self, **kwargs):
        self.client.delete(entity_id=self.entity_id, **kwargs)

    def update(self, **kwargs):
        new_params = {**self.entity, **kwargs}
        self._entity = self.client.update(self.entity_id, **new_params)
        return self.entity

    def _invalidate(self):
        self._entity = None


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
    def __init__(self, *args, entity_name='plan', entity_collection='plans', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.parent.url + '/application_plans'


class Accounts(DefaultClient):
    def __init__(self, *args, entity_name='account', entity_collection='accounts', **kwargs):
        super().__init__(*args, entity_name=entity_name,
                         entity_collection=entity_collection, **kwargs)

    @property
    def url(self):
        return self.threescale_client.admin_api_url + '/accounts'

    def create(self, params: dict = None, **kwargs) -> 'Account':
        return self.signup(params=params, **kwargs)

    def signup(self, params, **kwargs) -> 'Account':
        log.info(f"[SIGNUP] Create new Signup: {kwargs}")
        url = self.threescale_client.admin_api_url + '/signup'
        response = self.rest.post(url=url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance


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


# Resources

class ApplicationPlan(DefaultResource):
    pass


class Method(DefaultResource):
    pass


class Metric(DefaultResource):
    @property
    def methods(self) -> Methods:
        return Methods(parent=self, instance_klass=Method)


class Service(DefaultResource):
    @property
    def app_plans(self) -> ApplicationPlans:
        return ApplicationPlans(parent=self, instance_klass=ApplicationPlan)

    @property
    def metrics(self) -> Metrics:
        return Metrics(parent=self, instance_klass=Metric)


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
