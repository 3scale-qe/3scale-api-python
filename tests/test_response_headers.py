import os
import pytest
import threescale_api


@pytest.fixture(scope="module")
def cl():
    return threescale_api.ThreeScaleClient(url=os.environ['THREESCALE_PROVIDER_URL'],
                                         token=os.environ['THREESCALE_PROVIDER_TOKEN'],
                                           ssl_verify=False)


def test_x_served_by(cl):

    response = cl._rest.get(url=cl.url + '/admin/api/accounts')
    assert response.status_code == 200
    if "X-Served-By" in response.headers:
        assert True
    else:
        assert "X-Served-By" not in response.headers
