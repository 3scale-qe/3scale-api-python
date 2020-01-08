import pytest

from threescale_api import client


@pytest.fixture()
def url():
    return 'http://localhost'


@pytest.fixture()
def token():
    return 'test-token'


def _create_client(url, token, **kwargs) -> client.ThreeScaleClient:
    return client.ThreeScaleClient(url=url, token=token, **kwargs)


@pytest.fixture()
def api(url, token):
    return _create_client(url, token)


@pytest.mark.smoke
def test_api_client_initialization(api, url):
    assert api.url == url
    assert api.parent == api
    assert api.threescale_client == api
    assert api.admin_api_url == f'{url}/admin/api'
