import base64

import pytest


@pytest.fixture(scope="module")
def service_params(service_params):
    service_params.update(backend_version="2")
    return service_params


@pytest.fixture(scope="module")
def proxy(service, proxy):
    service.proxy.update(params={
        "credentials_location": "authorization"
    })


def test_app_key_authorization(proxy, application, ssl_verify):
    creds = application.authobj.credentials
    encoded = base64.b64encode(
        f"{creds['app_id']}:{creds['app_key']}".encode("utf-8")).decode("utf-8")

    response = application.test_request(verify=ssl_verify)

    assert response.status_code == 200
    assert response.request.headers["Authorization"] == "Basic %s" % encoded
