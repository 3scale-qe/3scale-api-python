import secrets

import pytest

from threescale import resources


@pytest.fixture(scope='module')
def resource_params() -> dict:
    suffix = secrets.token_urlsafe(8)
    name = f"test-{suffix}"
    return dict(name=name, org_name=name, username=name)


@pytest.fixture(scope='module')
def resource(api, resource_params) -> resources.Account:
    resource = api.accounts.create(params=resource_params)
    yield resource
    resource.delete()
    assert not resource.exists()


def test_accounts_list(api):
    services = api.accounts.list()
    assert len(services) > 1


def test_service_can_be_created(api, resource_params, resource):
    assert resource is not None
    assert resource.entity is not None
    assert resource.entity_id is not None
    assert resource['name'] == resource_params['name']
