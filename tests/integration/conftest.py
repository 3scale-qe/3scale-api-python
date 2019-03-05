import os
import secrets

import pytest
from dotenv import load_dotenv

import threescale

load_dotenv()


@pytest.fixture(scope='session')
def url() -> str:
    return os.getenv('THREESCALE_PROVIDER_URL')


@pytest.fixture(scope='session')
def token() -> str:
    return os.getenv('THREESCALE_PROVIDER_TOKEN')


@pytest.fixture(scope='session')
def master_url() -> str:
    return os.getenv('THREESCALE_MASTER_URL')


@pytest.fixture(scope='session')
def master_token() -> str:
    return os.getenv('THREESCALE_MASTER_TOKEN')


@pytest.fixture(scope='session')
def api(url, token) -> threescale.ThreeScaleClient:
    return threescale.ThreeScaleClient(url=url, token=token)


@pytest.fixture(scope='session')
def master_api(master_url: str, master_token: str) -> threescale.ThreeScaleClient:
    return threescale.ThreeScaleClient(url=master_url, token=master_token)


# Service

@pytest.fixture(scope='module')
def service_params():
    suffix = secrets.token_urlsafe(8)
    return dict(name=f"test-{suffix}")


@pytest.fixture(scope='module')
def service(service_params, api):
    service = api.services.create(params=service_params)
    yield service
    service.delete()
    assert not service.exists()


# Account
@pytest.fixture(scope='module')
def account_params():
    suffix = secrets.token_urlsafe(8)
    name = f"test-{suffix}"
    return dict(name=name, username=name, org_name=name)


@pytest.fixture(scope='module')
def account(account_params, api):
    entity = api.accounts.create(params=account_params)
    yield entity
    entity.delete()
    assert not entity.exists()


# Application plan
@pytest.fixture(scope='module')
def application_plan_params() -> dict:
    suffix = secrets.token_urlsafe(8)
    return dict(name=f"test-{suffix}")


@pytest.fixture(scope='module')
def application_plan(api, service, application_plan_params):
    resource = service.app_plans.create(params=application_plan_params)
    yield resource


# Application
@pytest.fixture(scope='module')
def application_params(application_plan):
    suffix = secrets.token_urlsafe(8)
    name = f"test-{suffix}"
    return dict(name=name, description=name, plan_id=application_plan['id'])


@pytest.fixture(scope='module')
def application(account, application_plan, application_params):
    resource = account.applications.create(params=application_params)
    yield resource
    resource.delete()
    assert not resource.exists()
