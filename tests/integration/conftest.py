import os
import secrets
from distutils.util import strtobool

import pytest
from dotenv import load_dotenv

import threescale

load_dotenv()


def get_suffix() -> str:
    return secrets.token_urlsafe(8)


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


@pytest.fixture(scope="session")
def ssl_verify() -> bool:
    return bool(strtobool(os.getenv('THREESCALE_SSL_VERIFY', False)))


@pytest.fixture(scope='session')
def api(url: str, token: str, ssl_verify: bool) -> threescale.ThreeScaleClient:
    return threescale.ThreeScaleClient(url=url, token=token, ssl_verify=ssl_verify)


@pytest.fixture(scope='session')
def master_api(master_url: str, master_token: str,
               ssl_verify: bool) -> threescale.ThreeScaleClient:
    return threescale.ThreeScaleClient(url=master_url, token=master_token, ssl_verify=ssl_verify)


@pytest.fixture(scope='module')
def service_params():
    suffix = get_suffix()
    return dict(name=f"test-{suffix}")


@pytest.fixture(scope='module')
def service(service_params, api):
    service = api.services.create(params=service_params)
    yield service
    service.delete()
    assert not service.exists()


@pytest.fixture(scope='module')
def account_params():
    suffix = get_suffix()
    name = f"test-{suffix}"
    return dict(name=name, username=name, org_name=name)


@pytest.fixture(scope='module')
def account(account_params, api):
    entity = api.accounts.create(params=account_params)
    yield entity
    entity.delete()
    assert not entity.exists()


@pytest.fixture(scope='module')
def application_plan_params() -> dict:
    suffix = get_suffix()
    return dict(name=f"test-{suffix}")


@pytest.fixture(scope='module')
def application_plan(api, service, application_plan_params):
    resource = service.app_plans.create(params=application_plan_params)
    yield resource


@pytest.fixture(scope='module')
def application_params(application_plan):
    suffix = get_suffix()
    name = f"test-{suffix}"
    return dict(name=name, description=name, plan_id=application_plan['id'])


@pytest.fixture(scope='module')
def application(account, application_plan, application_params):
    resource = account.applications.create(params=application_params)
    yield resource
    resource.delete()
    assert not resource.exists()


@pytest.fixture(scope='module')
def metric_params(service):
    suffix = get_suffix()
    friendly_name = f'test-{suffix}'
    system_name = f'{friendly_name}'.replace('-', '_')
    return dict(service_id=service['id'], friendly_name=friendly_name,
                system_name=system_name, unit='count')


@pytest.fixture(scope='module')
def metric(service, metric_params):
    resource = service.metrics.create(params=metric_params)
    yield resource
    resource.delete()
    assert not resource.exists()


@pytest.fixture(scope='module')
def method_params(service):
    suffix = get_suffix()
    friendly_name = f'test-method-{suffix}'
    system_name = f'{friendly_name}'.replace('-', '_')
    return dict(friendly_name=friendly_name, system_name=system_name, unit='hits')


@pytest.fixture
def updated_method_params(method_params):
    suffix = get_suffix()
    friendly_name = f'test-update-method-{suffix}'
    method_params['friendly_name'] = friendly_name
    method_params['system_name'] = f'{friendly_name}'.replace('-', '_')
    return method_params


@pytest.fixture(scope='module')
def hits_metric(service):
    return service.metrics.read_by(system_name='hits')


@pytest.fixture(scope='module')
def method(hits_metric, method_params):
    resource = hits_metric.methods.create(params=method_params)
    yield resource
    resource.delete()
    assert not resource.exists()
