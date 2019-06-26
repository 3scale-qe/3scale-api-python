import pytest
import backoff

from threescale_api.errors import ApiClientError

from tests.integration import asserts
from tests.integration.common import http_client


def test_should_create_metric(metric, metric_params):
    asserts.assert_resource(metric)
    asserts.assert_resource_params(metric, metric_params)


def test_should_fields_be_required(service):
    resource = service.metrics.create(params={}, throws=False)
    asserts.assert_errors_contains(resource, ['friendly_name', 'unit'])


def test_should_system_name_be_invalid(service, metric_params):
    metric_params['system_name'] = 'invalid name whitespaces'
    resource = service.metrics.create(params=metric_params, throws=False)
    asserts.assert_errors_contains(resource, ['system_name'])


def test_should_raise_exception(service):
    with pytest.raises(ApiClientError):
        service.metrics.create(params={})


def test_should_read_metric(metric, metric_params):
    resource = metric.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, metric_params)


def test_should_update_metric(metric, updated_metric_params):
    resource = metric.update(params=updated_metric_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, updated_metric_params)


def test_should_delete_metric(service, updated_metric_params):
    resource = service.metrics.create(params=updated_metric_params)
    assert resource.exists()
    resource.delete()
    assert not resource.exists()


def test_should_list_metrics(service):
    resources = service.metrics.list()
    assert len(resources) > 1


def test_should_return_auth_error_when_metric_is_disabled(
        service, metric_params, create_mapping_rule,
        account, ssl_verify, api_backend):
    """Metric is disabled when its limit is set to 0."""

    proxy = service.proxy.list()
    plan = service.app_plans.create(params=dict(name='metrics-disabled'))
    application_params = dict(name='metrics-disabled', plan_id=plan['id'],
                              description='metric disabled')
    app = account.applications.create(params=application_params)

    metric = service.metrics.create(params=metric_params)
    plan.limits(metric).create(params=dict(period='month', value=0))

    rules = proxy.mapping_rules.list()
    for rule in rules:
        rule.delete()
    rule = create_mapping_rule(metric, 'GET', '/foo/bah/')

    # update proxy after adding mapping rule
    # required for working
    service.proxy.update(params={'endpoint': 'http://test.test:80'})

    params = get_user_key_from_application(app, proxy)
    client = http_client(proxy['sandbox_endpoint'], ssl_verify, params=params)
    response = make_request(client, rule['pattern'])
    assert response.status_code == 403


@backoff.on_predicate(backoff.expo, lambda resp: resp.status_code == 200,
                      max_tries=8)
def make_request(client, path):
    return client.get(path=path)


def get_user_key_from_application(app, proxy):
    user_key = app['user_key']
    user_key_param = proxy['auth_user_key']
    return {user_key_param: user_key}

