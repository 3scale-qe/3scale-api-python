from tests.integration import asserts
from .asserts import assert_resource, assert_resource_params


def test_3scale_url_is_set(api, url, token):
    assert url is not None
    assert token is not None
    assert api.url is not None


def test_services_list(api):
    services = api.services.list()
    assert len(services) > 1


def test_service_can_be_created(api, service_params, service):
    assert_resource(service)
    assert_resource_params(service, service_params)


def test_service_can_be_read(api, service_params, service):
    read = api.services.read(service.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, service_params)


def test_service_can_be_read_by_name(api, service_params, service):
    account_name = service['system_name']
    read = api.services[account_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, service_params)


def test_service_can_be_updated(api, service):
    assert service['backend_version'] == '1'
    service['backend_version'] = '2'
    service.update()
    assert service['backend_version'] == '2'
    updated = service.read()
    assert updated['backend_version'] == '2'
    assert service['backend_version'] == '2'
