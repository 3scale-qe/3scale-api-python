import logging
from typing import Dict, List, Optional, TYPE_CHECKING, Union

import requests

from threescale_api import utils

if TYPE_CHECKING:
    from threescale_api.client import ThreeScaleClient, RestApiClient

log = logging.getLogger(__name__)


class DefaultClient:
    def __init__(self, parent=None, instance_klass=None,
                 entity_name: str = None, entity_collection: str = None):
        """Creates instance of the default client
        Args:
            parent: Parent resource or client
            instance_klass: Which class should be used to instantiate the resource
            entity_name(str): Entity name - required for extraction
            entity_collection(str): Collection name - required for extraction
        """
        self._parent = parent
        self._instance_klass = instance_klass
        self._entity_name = entity_name
        if entity_collection is None and entity_name is not None:
            entity_collection = f'{entity_name}s'
        self._entity_collection = entity_collection

    @property
    def url(self) -> str:
        """Default url for the resources collection
        Returns(str): URL
        """
        return self.threescale_client.admin_api_url

    @property
    def threescale_client(self) -> 'ThreeScaleClient':
        """Gets instance of the 3scale default client
        Returns(TheeScaleClient): 3scale client

        """
        return self.parent.threescale_client

    @property
    def parent(self) -> 'DefaultResource':
        """ Instance of the parent resource
        Returns(DefaultResource): Parent of the client is an subclass of the default resource

        """
        return self._parent

    @property
    def rest(self) -> 'RestApiClient':
        """Rest API client for the 3scale instance
        Returns(RestApiClient):

        """
        return self.threescale_client.rest

    def list(self, **kwargs) -> List['DefaultResource']:
        """List all entities
        Args:
            **kwargs: Optional parameters
        Returns(List['DefaultResource]): List of resources
        """
        log.info(self._log_message("[LIST] List", args=kwargs))
        instance = self._list(**kwargs)
        return instance

    def create(self, params: dict = None, **kwargs) -> 'DefaultResource':
        """Create a new instance
        Args:
            params: Parameters required to create new instance
            **kwargs: Optional parameters

        Returns:

        """
        log.info(self._log_message("[CREATE] Create new ", body=params, args=kwargs))
        url = self._entity_url()
        response = self.rest.post(url=url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance

    def delete(self, entity_id: int = None, **kwargs) -> bool:
        """Delete resource
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args

        Returns(bool): True if the resource has been successfully deleted
        """
        log.info(self._log_message("[DELETE] Delete ", entity_id=entity_id, args=kwargs))
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.delete(url=url, **kwargs)
        return response.ok

    def exists(self, entity_id=None, **kwargs) -> bool:
        """Check whether the resource exists
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args

        Returns(bool): True if the resource exists
        """
        log.info(self._log_message("[EXIST] Resource exist ", entity_id=entity_id, args=kwargs))
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.get(url=url, throws=False, **kwargs)
        return response.ok

    def update(self, entity_id=None, params: dict = None, **kwargs) -> 'DefaultResource':
        """Update resource
        Args:
            entity_id(int): Entity id
            params(dict): Params to be updated
            **kwargs: Optional args

        Returns(DefaultResource): Resource instance
        """
        log.info(self._log_message("[UPDATE] Update ", body=params,
                                   entity_id=entity_id, args=kwargs))
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.put(url=url, json=params, **kwargs)
        instance = self._create_instance(response=response)
        return instance

    def fetch(self, entity_id: int = None, **kwargs) -> dict:
        """Fetch the entity dictionary
        Args:
            entity_id(int): Entity id
            **kwargs: Optional args

        Returns(dict): Resource dict from the 3scale
        """
        log.debug(self._log_message("[FETCH] Fetch ", entity_id=entity_id, args=kwargs))
        url = self._entity_url(entity_id=entity_id)
        response = self.rest.get(url=url, **kwargs)
        return utils.extract_response(response=response, entity=self._entity_name)

    def __getitem__(self, selector: Union[int, 'str']) -> 'DefaultResource':
        """Gets the item
        Args:
            selector(Union[int, 'str']): Selector whether id or string
        Returns(DefaultResource): Resource instance
        """
        if isinstance(selector, int):
            return self.read(selector)
        return self.read_by_name(selector)

    def read(self, entity_id: int = None) -> 'DefaultResource':
        """Read the instance, read will just create empty resource and lazyloads only if needed
        Args:
            entity_id(int): Entity id
        Returns(DefaultResource): Default resource
        """
        log.debug(self._log_message("[READ] Read ", entity_id=entity_id))
        return self._instance_klass(client=self, entity_id=entity_id)

    def read_by_name(self, name: str, **kwargs) -> 'DefaultResource':
        """Read resource by name
        Args:
            name: Name of the resource (either system name, name, org_name ...)
            **kwargs:

        Returns:

        """
        for item in self._list(**kwargs):
            if item.entity_name and item.entity_name == name:
                return item

    def select(self, predicate, **kwargs) -> List['DefaultResource']:
        """Select resource s based on the predicate
        Args:
            predicate: Predicate
            **kwargs: Optional args
        Returns: List of resources
        """
        return [item for item in self._list(**kwargs) if predicate(item)]

    def select_by(self, **params) -> List['DefaultResource']:
        """Select by params - logical and
        Args:
            **params: params used for selection
        Returns: List of resources
        """
        log.debug(f"[SELECT] By params: {params}")

        def predicate(item):
            for (key, val) in params.items():
                if item[key] != val:
                    return False
            return True

        return self.select(predicate=predicate)

    def read_by(self, **params) -> 'DefaultResource':
        """Read by params - it will return just one instance of the resource
        Args:
            **params: params used for selection
        Returns(DefaultResource): Resource instance
        """
        result = self.select_by(**params)
        return result[0] if result else None

    def _log_message(self, message, entity_id=None, body=None, args=None) -> str:
        msg = f"{message} {self._instance_klass.__name__}"
        if entity_id:
            msg += f"({entity_id}))"
        if body:
            msg += f" {body}"
        if args:
            msg += f" args={args}"
        return msg

    def _list(self, **kwargs) -> List['DefaultResource']:
        """Internal list implementation used in list or `select` methods
        Args:
            **kwargs: Optional parameters

        Returns(List['DefaultResource']):

        """
        url = self._entity_url()
        response = self.rest.get(url=url, **kwargs)
        instance = self._create_instance(response=response, collection=True)
        return instance

    def _entity_url(self, entity_id=None) -> str:
        if not entity_id:
            return self.url
        return self.url + '/' + str(entity_id)

    def _create_instance(self, response: requests.Response, klass=None, collection: bool = False):
        klass = klass or self._instance_klass
        extracted = self._extract_resource(response, collection)
        instance = self._instantiate(extracted=extracted, klass=klass)
        log.debug(f"[INSTANCE] Created instance: {instance}")
        return instance

    def _extract_resource(self, response, collection) -> Union[List, Dict]:
        extract_params = dict(response=response, entity=self._entity_name)
        if collection:
            extract_params['collection'] = self._entity_collection
        extracted = utils.extract_response(**extract_params)
        return extracted

    def _instantiate(self, extracted, klass):
        if isinstance(extracted, list):
            instance = [self.__make_instance(item, klass) for item in extracted]
            return instance
        return self.__make_instance(extracted, klass)

    def __make_instance(self, extracted: dict, klass):
        instance = klass(client=self, entity=extracted) if klass else extracted
        return instance


class DefaultResource:
    def __init__(self, client: DefaultClient = None, entity_id: int = None, entity_name: str = None,
                 entity: dict = None):
        """Create instance of the resource
        Args:
            client: Client instance of the resource
            entity_id(int): Entity id
            entity_name(str): Entity name field (system_name or name ...)
            entity(dict): Entity instance
        """
        self._entity_id = entity_id or entity.get('id')
        self._entity = entity
        self._client = client
        self._entity_name = entity_name

    @property
    def threescale_client(self) -> 'ThreeScaleClient':
        return self.client.threescale_client

    @property
    def parent(self) -> 'DefaultResource':
        return self.client.parent

    @property
    def entity_name(self) -> Optional[str]:
        return self[self._entity_name]

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
            self._entity = self.fetch(**kwargs)
        return self

    def read(self, **kwargs) -> 'DefaultResource':
        self._invalidate()
        self._lazy_load(**kwargs)
        return self

    def fetch(self, **kwargs) -> dict:
        return self.client.fetch(self.entity_id, **kwargs)

    def exists(self, **kwargs) -> bool:
        return self.client.exists(entity_id=self.entity_id, **kwargs)

    def delete(self, **kwargs):
        self.client.delete(entity_id=self.entity_id, **kwargs)

    def update(self, **kwargs) -> 'DefaultResource':
        new_params = {**self.entity, **kwargs}
        new_entity = self.client.update(entity_id=self.entity_id, params=new_params)
        self._entity = new_entity.entity
        return self

    def _invalidate(self):
        self._entity = None


class DefaultPlanClient(DefaultClient):
    def set_default(self, entity_id: int, **kwargs) -> 'DefaultPlanResource':
        """Sets default plan for the entity
        Args:
            entity_id: Entity id
            **kwargs: Optional args
        Returns(DefaultPlanResource):
        """
        log.info(self._log_message("[PLAN] Set default ", entity_id=entity_id, args=kwargs))
        url = self._entity_url(entity_id) + '/default'
        response = self.rest.put(url=url, **kwargs)
        instance = self._create_instance(response=response)
        return instance

    def get_default(self, **kwargs) -> Optional['DefaultResource']:
        """Get default plan if set
        Args:
            **kwargs: Optional arguments
        Returns(DefaultResource): Resource instance
        """
        default = self.select(lambda x: x.is_default, **kwargs)
        if default:
            return default[0]
        return None


class DefaultPlanResource(DefaultResource):
    def __init__(self, entity_name='system_name', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    def set_default(self, **kwargs) -> 'DefaultStateResource':
        """Set the plan default
        Args:
            **kwargs: Optional args
        Returns(DefaultStateResource): State resource instance
        """
        return self.client.set_default(entity_id=self.entity_id, **kwargs)

    @property
    def is_default(self) -> bool:
        return self['default'] is True


class DefaultStateClient(DefaultClient):
    def set_state(self, entity_id, state: str, **kwargs):
        """Sets the state for the resource
        Args:
            entity_id(int): Entity id
            state(str): Which state
            **kwargs: Optional args

        Returns(DefaultStateResource): State resource instance
        """
        log.info(self._log_message("[STATE] Set state ", body=f"[{state}]", args=kwargs))
        url = self._entity_url(entity_id) + '/' + state
        response = self.rest.put(url=url, **kwargs)
        instance = self._create_instance(response=response)
        return instance


class DefaultStateResource(DefaultResource):
    def set_state(self, state: str, **kwargs) -> 'DefaultStateResource':
        """Sets the state for the resource
        Args:
            state(str): Which state
            **kwargs: Optional args

        Returns(DefaultStateResource): State resource instance
        """
        return self.client.set_state(entity_id=self.entity_id, state=state, **kwargs)


class DefaultUserResource(DefaultStateResource):
    def __init__(self, entity_name='username', **kwargs):
        super().__init__(entity_name=entity_name, **kwargs)

    def suspend(self, **kwargs) -> 'DefaultUserResource':
        """Suspends the user
        Args:
            **kwargs: Optional arguments
        Returns(DefaultUserResource): User instance

        """
        return self.set_state(state='suspend', **kwargs)

    def resume(self, **kwargs):
        """Resumes the user
        Args:
            **kwargs: Optional arguments
        Returns(DefaultUserResource): User instance

        """
        return self.set_state(state='resume', **kwargs)

    def activate(self, **kwargs):
        """Activates the user
        Args:
            **kwargs: Optional arguments
        Returns(DefaultUserResource): User instance

        """
        return self.set_state(state='activate', **kwargs)

    def set_as_admin(self, **kwargs):
        """Promotes the user to admin
        Args:
            **kwargs: Optional arguments
        Returns(DefaultUserResource): User instance

        """
        return self.set_state(state='set_as_admin', **kwargs)

    def set_as_member(self, **kwargs):
        """Demotes the user to s member
        Args:
            **kwargs: Optional arguments
        Returns(DefaultUserResource): User instance

        """
        return self.set_state(state='set_as_member', **kwargs)
