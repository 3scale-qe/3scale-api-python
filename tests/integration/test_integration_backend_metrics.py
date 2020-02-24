import pytest
import backoff

from threescale_api.errors import ApiClientError

from tests.integration import asserts


def test_should_create_metric(backend_metric, backend_metric_params):
    asserts.assert_resource(backend_metric)
    asserts.assert_resource_params(backend_metric, backend_metric_params)

def test_should_fields_be_required(backend):
    resource = backend.metrics.create(params={}, throws=False)
    asserts.assert_errors_contains(resource, ['friendly_name', 'unit'])


def test_should_system_name_be_invalid(backend, backend_metric_params):
    backend_metric_params['system_name'] = 'invalid name whitespaces'
    resource = backend.metrics.create(params=backend_metric_params, throws=False)
    asserts.assert_errors_contains(resource, ['system_name'])


def test_should_raise_exception(backend):
    with pytest.raises(ApiClientError):
        backend.metrics.create(params={})


def test_should_read_metric(backend_metric, backend_metric_params):
    resource = backend_metric.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_metric_params)


def test_should_update_metric(backend_metric, backend_updated_metric_params):
    resource = backend_metric.update(params=backend_updated_metric_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_updated_metric_params)


def test_should_delete_metric(backend, backend_updated_metric_params):
    resource = backend.metrics.create(params=backend_updated_metric_params)
    assert resource.exists()
    resource.delete()
    assert not resource.exists()


def test_should_list_metrics(backend):
    resources = backend.metrics.list()
    assert len(resources) > 1

def test_should_apicast_return_403_when_metric_is_disabled(
        service, backend_metric_params, create_backend_mapping_rule,
        account, ssl_verify, backend, backend_usage):
    """Metric is disabled when its limit is set to 0."""

    proxy = service.proxy.list()
    plan = service.app_plans.create(params=dict(name='metrics-disabled'))
    application_params = dict(name='metrics-disabled', plan_id=plan['id'],
                              description='metric disabled')
    app = account.applications.create(params=application_params)

    back_metric = backend.metrics.create(params=backend_metric_params)
    plan.limits(back_metric).create(params=dict(period='month', value=0))

    rules = backend.mapping_rules.list()
    for rule in rules:
        rule.delete()
    rule = create_backend_mapping_rule(back_metric, 'GET', '/foo/bah/')

    proxy = service.proxy.list()
    proxy.deploy()

    params = get_user_key_from_application(app, proxy)
    client = app.api_client(verify=ssl_verify)
    response = make_request(client, backend_usage['path'] + '/' + rule['pattern'])
    assert response.status_code == 403


@backoff.on_predicate(backoff.expo, lambda resp: resp.status_code == 200,
                      max_tries=8)
def make_request(client, path):
    return client.get(path=path)


def get_user_key_from_application(app, proxy):
    user_key = app['user_key']
    user_key_param = proxy['auth_user_key']
    return {user_key_param: user_key}


def update_proxy_endpoint(service):
    """Update service proxy.

    Bug that if the proxy is not updated the changes applied
    to the mapping rules dont take effect."""
    service.proxy.update(params={'endpoint': 'http://test.test:80'})

def test_should_apicast_return_429_when_limits_exceeded(
        service, application_plan, create_mapping_rule,
        apicast_http_client):
    metric_params = dict(system_name='limits_exceeded', unit='count',
                         friendly_name='Limits Exceeded')
    metric = service.metrics.create(params=metric_params)
    application_plan.limits(metric).create(params=dict(period='day', value=1))

    rule = create_mapping_rule(metric, 'GET', '/limits/exceeded/')

    update_proxy_endpoint(service)

    response = apicast_http_client.get(path=rule['pattern'])
    while response.status_code == 200:
        response = apicast_http_client.get(path=rule['pattern'])

    assert response.status_code == 429
