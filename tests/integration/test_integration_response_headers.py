
def test_x_served_by(api):
    response = api._rest.get(url=api.admin_api_url + '/accounts')
    assert response.status_code == 200
    assert "X-Served-By" not in response.headers
    