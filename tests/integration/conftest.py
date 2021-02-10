import os
import secrets
import time
from distutils.util import strtobool

import pytest
from dotenv import load_dotenv
from threescale_api import errors

import threescale_api
from threescale_api.resources import (Service, ApplicationPlan, Application,
                                      Proxy, Backend, Metric, MappingRule,
                                      BackendMappingRule, BackendUsage,
                                      ActiveDoc, Webhooks)

load_dotenv()

def cleanup(resource):
    resource.delete()
    assert not resource.exists()

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
    ssl_verify = os.getenv('THREESCALE_SSL_VERIFY', 'false')
    return bool(strtobool(ssl_verify))


@pytest.fixture(scope='session')
def api_backend() -> str:
    return os.getenv('TEST_API_BACKEND', 'http://www.httpbin.org:80')


@pytest.fixture(scope='session')
def api(url: str, token: str,
        ssl_verify: bool) -> threescale_api.ThreeScaleClient:
    return threescale_api.ThreeScaleClient(url=url, token=token,
                                           ssl_verify=ssl_verify)


@pytest.fixture(scope='session')
def master_api(master_url: str, master_token: str,
               ssl_verify: bool) -> threescale_api.ThreeScaleClient:
    return threescale_api.ThreeScaleClient(url=master_url, token=master_token,
                                           ssl_verify=ssl_verify)


@pytest.fixture(scope='module')
def apicast_http_client(application, ssl_verify):
    return application.api_client(verify=ssl_verify)


@pytest.fixture(scope='module')
def service_params():
    suffix = get_suffix()
    return dict(name=f"test-{suffix}")


@pytest.fixture(scope='module')
def service(service_params, api) -> Service:
    service = api.services.create(params=service_params)
    yield service
    cleanup(service)


@pytest.fixture(scope='module')
def account_params():
    suffix = get_suffix()
    name = f"test-{suffix}"
    return dict(name=name, username=name, org_name=name)


@pytest.fixture(scope='module')
def account(account_params, api):
    entity = api.accounts.create(params=account_params)
    yield entity
    cleanup(entity)


@pytest.fixture(scope='module')
def application_plan_params() -> dict:
    suffix = get_suffix()
    return dict(name=f"test-{suffix}")


@pytest.fixture(scope='module')
def application_plan(api, service, application_plan_params) -> ApplicationPlan:
    resource = service.app_plans.create(params=application_plan_params)
    yield resource


@pytest.fixture(scope='module')
def application_params(application_plan):
    suffix = get_suffix()
    name = f"test-{suffix}"
    return dict(name=name, description=name, plan_id=application_plan['id'])


@pytest.fixture(scope='module')
def application(account, application_plan, application_params) -> Application:
    resource = account.applications.create(params=application_params)
    yield resource
    cleanup(resource)


@pytest.fixture(scope='module')
def proxy(service, application, api_backend) -> Proxy:
    params = {
        'api_backend': api_backend,
        'credentials_location': 'query',
        'api_test_path': '/get',
    }
    proxy = service.proxy.update(params=params)
    return proxy


@pytest.fixture(scope='module')
def backend_usage(service, backend, application) -> BackendUsage:
    params = {
        'service_id': service['id'],
        'backend_api_id': backend['id'],
        'path': '/get',
    }
    resource = service.backend_usages.create(params=params)
    yield resource
    cleanup(resource)

@pytest.fixture(scope='module')
def metric_params(service):
    suffix = get_suffix()
    friendly_name = f'test-metric-{suffix}'
    system_name = f'{friendly_name}'.replace('-', '_')
    return dict(service_id=service['id'], friendly_name=friendly_name,
                system_name=system_name, unit='count')

@pytest.fixture(scope='module')
def backend_metric_params(backend):
    suffix = get_suffix()
    friendly_name = f'test-metric-{suffix}'
    system_name = f'{friendly_name}'.replace('-', '_')
    return dict(backend_id=backend['id'], friendly_name=friendly_name,
                system_name=system_name, unit='count')

@pytest.fixture
def updated_metric_params(metric_params):
    suffix = get_suffix()
    friendly_name = f'test-updated-metric-{suffix}'
    metric_params['friendly_name'] = f'/anything/{friendly_name}'
    metric_params['system_name'] = friendly_name.replace('-', '_')
    return metric_params

@pytest.fixture
def backend_updated_metric_params(backend_metric_params):
    suffix = get_suffix()
    friendly_name = f'test-updated-metric-{suffix}'
    backend_metric_params['friendly_name'] = f'/anything/{friendly_name}'
    backend_metric_params['system_name'] = friendly_name.replace('-', '_')
    return backend_metric_params



@pytest.fixture(scope='module')
def metric(service, metric_params) -> Metric:
    resource = service.metrics.create(params=metric_params)
    yield resource
    cleanup(resource)


@pytest.fixture(scope='module')
def hits_metric(service):
    return service.metrics.read_by(system_name='hits')


@pytest.fixture(scope='module')
def method_params(service):
    suffix = get_suffix()
    friendly_name = f'test-method-{suffix}'
    system_name = f'{friendly_name}'.replace('-', '_')
    return dict(friendly_name=friendly_name, system_name=system_name,
                unit='hits')


@pytest.fixture
def updated_method_params(method_params):
    suffix = get_suffix()
    friendly_name = f'test-updated-method-{suffix}'
    method_params['friendly_name'] = friendly_name
    method_params['system_name'] = f'{friendly_name}'.replace('-', '_')
    return method_params


@pytest.fixture(scope='module')
def method(hits_metric, method_params):
    resource = hits_metric.methods.create(params=method_params)
    yield resource
    cleanup(resource)


def get_mapping_rule_pattern():
    suffix = get_suffix()
    pattern = f'test-{suffix}'.replace('_', '-')
    return pattern


@pytest.fixture(scope='module')
def mapping_rule_params(hits_metric):
    """
    Fixture for getting paramteres for mapping rule for product/service.
    """
    return dict(http_method='GET', pattern='/', metric_id=hits_metric['id'],
                delta=1)


@pytest.fixture(scope='module')
def backend_mapping_rule_params(backend_metric):
    """
    Fixture for getting paramteres for mapping rule for backend.
    """
    return dict(http_method='GET', pattern='/get/anything/id', metric_id=backend_metric['id'],
                delta=1)

@pytest.fixture
def updated_mapping_rules_params(mapping_rule_params):
    """
    Fixture for updating mapping rule for product/service.
    """
    pattern = get_mapping_rule_pattern()
    params = mapping_rule_params.copy()
    params['pattern'] = f'/get/anything/{pattern}'
    return params

@pytest.fixture
def updated_backend_mapping_rules_params(backend_mapping_rule_params):
    """
    Fixture for updating mapping rule for backend.
    """
    pattern = get_mapping_rule_pattern()
    params = backend_mapping_rule_params.copy()
    params['pattern'] = f'/get/anything/{pattern}'
    return params


@pytest.fixture(scope='module')
def mapping_rule(proxy, mapping_rule_params) -> MappingRule:
    """
    Fixture for getting mapping rule for product/service.
    """
    resource = proxy.mapping_rules.create(params=mapping_rule_params)
    yield resource
    cleanup(resource)

@pytest.fixture(scope='module')
def backend_mapping_rule(backend, backend_mapping_rule_params) -> BackendMappingRule:
    """
    Fixture for getting mapping rule for backend.
    """
    resource = backend.mapping_rules.create(params=backend_mapping_rule_params)
    yield resource
    cleanup(resource)

@pytest.fixture
def create_mapping_rule(service):
    """
    Fixture for creating mapping rule for product/service.
    """
    rules = []
    proxy = service.proxy.list()

    def _create(metric, http_method, path):
        params = dict(service_id=service['id'],
                      http_method=http_method,
                      pattern=f'/anything{path}',
                      delta=1, metric_id=metric['id'])
        rule = proxy.mapping_rules.create(params=params)
        rules.append(rule)
        return rule

    yield _create

    for rule in rules:
        if rule.exists():
            cleanup(rule)

@pytest.fixture
def create_backend_mapping_rule(backend):
    """
    Fixture for creating mapping rule for backend.
    """
    rules = []

    def _create(backend_metric, http_method, path):
        params = dict(backend_id=backend['id'],
                      http_method=http_method,
                      pattern=f'/anything{path}',
                      delta=1, metric_id=backend_metric['id'])
        rule = backend.mapping_rules.create(params=params)
        rules.append(rule)
        return rule

    yield _create

    for rule in rules:
        if rule.exists():
            cleanup(rule)

@pytest.fixture(scope='module')
def backend_params(api_backend):
    """
    Fixture for getting backend parameters.
    """
    suffix = get_suffix()
    return dict(name=f"test-backend-{suffix}",
                private_endpoint=api_backend,
                description='111')

@pytest.fixture(scope='module')
def backend(backend_params, api) -> Backend:
    """
    Fixture for getting backend.
    """
    backend = api.backends.create(params=backend_params)
    yield backend
    cleanup(backend)

@pytest.fixture(scope='module')
def backend_metric(backend, metric_params) -> Metric:
    """
    Fixture for getting backend metric.
    """
    resource = backend.metrics.create(params=metric_params)
    yield resource
    cleanup(resource)

@pytest.fixture(scope="module")
def custom_tenant(master_api, tenant_params):
    """
    Fixture for getting the custom tenant.
    """
    resource = master_api.tenants.create(tenant_params)
    yield resource
    resource.delete()
    # tenants are not deleted immediately, they are scheduled for the deletion
    # the exists method returns ok response, even if the tenant is scheduled for deletion
    # However, the deletion of the tenant fails, if already deleted
    with pytest.raises(errors.ApiClientError):
        resource.delete()

@pytest.fixture(scope="module")
def tenant_params():
    """
    Params for custom tenant
    """
    return dict(username="tenant",
                password="123456",
                email="email@invalid.invalid",
                org_name="org")

@pytest.fixture(scope='module')
def active_docs_body():
    return """
{"swagger":"2.0","info":{"version":"1.0.0","title":"Test"},"paths":{"/test":{"get":{"operationId":"Test",
"parameters":[],"responses":{"400":{"description":"bad input parameter"}}}}},"definitions":{}}
"""

@pytest.fixture(scope='module')
def active_docs_params(active_docs_body):
    suffix = get_suffix()
    name = f"test-{suffix}"
    return dict(name=name, body=active_docs_body)


@pytest.fixture(scope='module')
def active_doc(api, service, active_docs_params) -> ActiveDoc:
    """
    Fixture for getting active doc.
    """
    acs = active_docs_params.copy()
    acs['service_id'] = service['id']
    resource = api.active_docs.create(params=acs)
    yield resource
    cleanup(resource)


@pytest.fixture(scope='module')
def provider_account_params():
    suffix = get_suffix()
    name = f"test-{suffix}"
    return dict(username=name,
                email=f'{name}@example.com',
                assword='123456')


@pytest.fixture(scope='module')
def provider_account(provider_account_params, api):
    entity = api.provider_accounts.create(params=provider_account_params)
    yield entity
    cleanup(entity)


@pytest.fixture(scope='module')
def webhook(api):
    return api.webhooks


@pytest.fixture(scope='module')
def account_plans_params():
    suffix = get_suffix()
    name = f"test-{suffix}"
    return dict(name=name)


@pytest.fixture(scope='module')
def account_plan(account_plans_params, api):
    entity = api.account_plans.create(params=account_plans_params)
    yield entity
    cleanup(entity)
