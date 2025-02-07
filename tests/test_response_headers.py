import threescale_api
import os
import pytest

@pytest.fixture(scope="module")
def client():
    return threescale_api.ThreeScaleClient(url=os.environ['THREESCALE_PROVIDER_URL'],
                                         token=os.environ['THREESCALE_PROVIDER_TOKEN'], ssl_verify=False)

def test_x_served_by_ga(client):
    response = client._rest.get(url=client.url + "/accounts.json")
    assert response.status_code == 200
    assert "X-Served-By" not in response.headers

def test_x_served_by_mas(client):
    response = client._rest.get(url=client.url + "/accounts.json")
    assert response.status_code == 200
    assert "X-Served-By" in response.headers