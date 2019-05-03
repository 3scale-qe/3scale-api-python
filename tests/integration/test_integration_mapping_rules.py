import pytest
import requests

from tests.integration import asserts


def test_should_list_mapping_rules(proxy, mapping_rule):
    resource = proxy.mapping_rules.list()
    assert len(resource) > 1


def test_should_create_mapping_rule(mapping_rule, mapping_rule_params):
    asserts.assert_resource(mapping_rule)
    asserts.assert_resource_params(mapping_rule, mapping_rule_params)


def test_should_mapping_rule_endpoint_return_ok(mapping_rule, apicast_http_client):
    response = apicast_http_client.get(path=mapping_rule['pattern'])
    asserts.assert_http_ok(response)


def test_should_fields_be_required(proxy, updated_mapping_rules_params):
    del updated_mapping_rules_params['delta']
    del updated_mapping_rules_params['http_method']
    del updated_mapping_rules_params['metric_id']
    resource = proxy.mapping_rules.create(params=updated_mapping_rules_params, throws=False)
    asserts.assert_errors_contains(resource, ['delta', 'http_method', 'metric_id'])


def test_should_read_mapping_rule(mapping_rule, mapping_rule_params):
    resource = mapping_rule.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, mapping_rule_params)


def test_should_update_mapping_rule(proxy, updated_mapping_rules_params, apicast_http_client):
    resource = proxy.mapping_rules.create(params=updated_mapping_rules_params)
    pattern = '/anything/test-foo'
    resource['pattern'] = pattern
    resource.update()
    updated_resource = resource.read()
    assert updated_resource['pattern'] == pattern
    response = apicast_http_client.get(path=pattern)
    asserts.assert_http_ok(response)


def test_should_delete_mapping_rule(proxy, updated_mapping_rules_params):
    resource = proxy.mapping_rules.create(params=updated_mapping_rules_params)
    assert resource.exists()
    resource.delete()
    assert not resource.exists()


def test_stop_processing_mapping_rules_once_first_one_is_met(proxy, updated_mapping_rules_params,
                                                             apicast_http_client):
    params_first = updated_mapping_rules_params.copy()
    params_first['pattern'] = '/anything/search'
    resource_first = proxy.mapping_rules.create(params=params_first)
    assert resource_first.exists()

    params_second = updated_mapping_rules_params.copy()
    params_second['pattern'] = '/anything/{id}'
    resource_second =proxy.mapping_rules.create(params=params_second)
    assert resource_second.exists()

    response = apicast_http_client.get(path=params_first['pattern'])
    asserts.assert_http_ok(response)

    assert params_first['pattern'] in response.url
