import pytest

from threescale_api.errors import ApiClientError

from tests.integration import asserts


def test_should_create_method(method, method_params):
    asserts.assert_resource(method)
    asserts.assert_resource_params(method, method_params)


def test_should_not_create_method_for_custom_metric(metric, method_params):
    resource = metric.methods.create(params=method_params, throws=False)
    asserts.assert_errors_contains(resource, ['parent_id'])


def test_should_friendly_name_be_required(hits_metric):
    resource = hits_metric.methods.create(params={}, throws=False)
    asserts.assert_errors_contains(resource, ['friendly_name'])


def test_should_raise_api_exception(hits_metric):
    with pytest.raises(ApiClientError):
        hits_metric.methods.create(params={})


def test_should_read_method(method, method_params):
    resource = method.read()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, method_params)


def test_should_update_method(method, updated_method_params):
    resource = method.update(params=updated_method_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, updated_method_params)


def test_should_delete_method(hits_metric, updated_method_params):
    resource = hits_metric.methods.create(params=updated_method_params)
    assert resource.exists()
    resource.delete()
    assert not resource.exists()


def test_should_list_methods(hits_metric):
    resources = hits_metric.methods.list()
    assert len(resources) == 1
