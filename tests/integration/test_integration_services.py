import secrets

import pytest

from threescale import resources
from .utils import assert_resource_params


@pytest.fixture(scope='module')
def resource_params():
    suffix = secrets.token_urlsafe(8)
    return dict(name=f"test-{suffix}")


@pytest.fixture(scope='module')
def resource(api, resource_params) -> resources.Service:
    resource = api.services.create(params=resource_params)
    yield resource
    resource.delete()
    assert not resource.exists()


def test_3scale_url_is_set(api, url, token):
    assert url is not None
    assert token is not None
    assert api.url is not None


def test_services_list(api):
    services = api.services.list()
    assert len(services) > 1


def test_service_can_be_created(api, resource_params, resource):
    assert resource is not None
    assert resource.entity is not None
    assert resource.entity_id is not None
    assert_resource_params(resource, resource_params)
