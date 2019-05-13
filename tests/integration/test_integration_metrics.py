import pytest

from threescale_api.errors import ApiClientError

from tests.integration import asserts


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
