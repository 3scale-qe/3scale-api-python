from tests.integration import asserts
from threescale_api.resources import Backends
from .asserts import assert_resource, assert_resource_params


def test_3scale_url_is_set(api, url, token):
    assert url is not None
    assert token is not None
    assert api.url is not None


def test_backends_list(api):
    backends = api.backends.list()
    assert len(backends) >= 1


def test_backend_can_be_created(api, backend_params, backend):
    assert_resource(backend)
    assert_resource_params(backend, backend_params)


def test_backend_can_be_read(api, backend_params, backend):
    read = api.backends.read(backend.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, backend_params)


def test_backend_can_be_read_by_name(api, backend_params, backend):
    backend_name = backend['system_name']
    read = api.backends[backend_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, backend_params)


def test_backend_can_be_updated(api, backend):
    assert backend['description'] == '111'
    backend['description'] = '222'
    backend.update()
    assert backend['description'] == '222'
    updated = backend.read()
    assert updated['description'] == '222'
    assert backend['description'] == '222'


def test_backend_metrics_list(backend, backend_metric):
    assert len(backend.metrics.list()) > 1


def test_backend_mapping_rules_list(backend, backend_mapping_rule):
    assert backend.mapping_rules.list()
