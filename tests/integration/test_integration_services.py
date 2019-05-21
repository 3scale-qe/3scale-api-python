from tests.integration import asserts
from threescale_api.resources import Proxy, Service
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


def test_service_get_proxy(api, service: Service, proxy: Proxy, api_backend):
    assert proxy['api_backend'] == api_backend
    assert proxy['api_test_path'] == '/get'


def test_service_set_proxy(api, service: Service, proxy: Proxy, api_backend):
    updated = proxy.update(params=dict(api_test_path='/ip'))
    assert updated['api_backend'] == api_backend
    assert updated['api_test_path'] == '/ip'


def test_service_proxy_promote(service, proxy):
    res = proxy.promote()
    assert res is not None
    assert res['environment'] == 'production'
    assert res['content'] is not None


def test_service_list_configs(service, proxy):
    res = proxy.configs.list(env='staging')
    assert res
    item = res[0]
    assert item
