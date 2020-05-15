import pytest


@pytest.fixture(scope="module")
def service_params(service_params):
    service_params.update(backend_version="2")
    return service_params


def test_user_key(proxy, apicast_http_client):
    assert apicast_http_client.get("/get").status_code == 200
