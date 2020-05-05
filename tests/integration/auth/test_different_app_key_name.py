import pytest


@pytest.fixture(scope="module")
def service_params(service_params):
    service_params.update(backend_version="2")
    return service_params


@pytest.fixture(scope="module")
def proxy(service, proxy):
    service.proxy.update(params={
        "auth_app_key": "akey",
        "auth_app_id": "aid",
    })


def test_different_user_key(proxy, application, ssl_verify):
    client = application.api_client(verify=ssl_verify)

    response = client.get("/get")
    assert response.status_code == 200
    assert "akey" in response.request.url
    assert "aid" in response.request.url
