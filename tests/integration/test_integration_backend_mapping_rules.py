import pytest

from tests.integration import asserts


def test_should_list_mapping_rules(backend, backend_mapping_rule):
    resource = backend.mapping_rules.list()
    assert resource

def test_should_create_mapping_rule(backend_mapping_rule, backend_mapping_rule_params):
    asserts.assert_resource(backend_mapping_rule)
    asserts.assert_resource_params(backend_mapping_rule, backend_mapping_rule_params)

def test_should_mapping_rule_endpoint_return_ok(service,
        backend_mapping_rule, backend_usage, apicast_http_client):
    service.proxy.deploy()

    response = apicast_http_client.get(path=backend_mapping_rule['pattern'])
    asserts.assert_http_ok(response)


def test_should_fields_be_required(backend, updated_backend_mapping_rules_params):
    del updated_backend_mapping_rules_params['delta']
    del updated_backend_mapping_rules_params['http_method']
    del updated_backend_mapping_rules_params['metric_id']
    resource = backend.mapping_rules.create(params=updated_backend_mapping_rules_params, throws=False)
    asserts.assert_errors_contains(resource, ['delta', 'http_method', 'metric_id'])

def test_should_read_mapping_rule(backend_mapping_rule, backend_mapping_rule_params):
    resource = backend_mapping_rule.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, backend_mapping_rule_params)


def test_should_update_mapping_rule(service,
        backend, backend_usage, updated_backend_mapping_rules_params, apicast_http_client):
    resource = backend.mapping_rules.create(updated_backend_mapping_rules_params)
    pattern = '/get/anything/test-foo'
    resource['pattern'] = pattern
    resource.update()
    updated_resource = resource.read()
    assert updated_resource['pattern'] == pattern

    service.proxy.deploy()

    response = apicast_http_client.get(path=pattern)
    asserts.assert_http_ok(response)


def test_should_delete_mapping_rule(backend, updated_backend_mapping_rules_params):
    resource = backend.mapping_rules.create(params=updated_backend_mapping_rules_params)
    assert resource.exists()
    resource.delete()
    assert not resource.exists()


def test_stop_processing_mapping_rules_once_first_one_is_met(service,
        backend_usage, backend, updated_backend_mapping_rules_params, apicast_http_client):
    params_first = updated_backend_mapping_rules_params.copy()
    params_first['pattern'] = '/get/anything/search'
    resource_first = backend.mapping_rules.create(params=params_first)
    assert resource_first.exists()

    params_second = updated_backend_mapping_rules_params.copy()
    params_second['pattern'] = '/get/anything/{id}'
    resource_second = backend.mapping_rules.create(params=params_second)
    assert resource_second.exists()

    service.proxy.deploy()

    response = apicast_http_client.get(path=params_first['pattern'])
    asserts.assert_http_ok(response)

    assert params_first['pattern'] in response.url
