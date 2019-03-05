from .asserts import assert_resource_params, assert_resource


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
