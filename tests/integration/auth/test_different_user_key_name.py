import pytest


@pytest.fixture(scope="module")
def proxy(service, proxy):
    service.proxy.update(params={"auth_user_key": "ukey"})


def test_different_user_key(proxy, application, ssl_verify):
    client = application.api_client(verify=ssl_verify)

    response = client.get("/get")
    assert response.status_code == 200
    assert "ukey" in response.request.url
