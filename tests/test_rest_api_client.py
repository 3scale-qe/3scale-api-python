import pytest
import responses

from threescale import client, errors


@pytest.fixture()
def url():
    return 'http://localhost'


@pytest.fixture()
def token():
    return 'test-token'


@pytest.fixture()
def access_token(token):
    return dict(access_token=token)


@pytest.fixture()
def rest(url, token):
    return client.RestApiClient(url=url, token=token)


def test_rest_api_initialization(rest, url):
    assert rest.url == url


@responses.activate
def test_404_response(rest, url, token):
    responses.add(responses.GET, f'{url}.json',
                  json={'error': 'not found'}, status=404)

    with pytest.raises(errors.ApiClientError):
        rest.request()


@responses.activate
def test_get_response(rest, url, token):
    add_response(responses.GET, url)

    resp = rest.get(path='/some')
    assert_valid_message(resp=resp, url=url, token=token, method='GET')


@responses.activate
def test_delete_response(rest, url, token):
    add_response(responses.DELETE, url)

    resp = rest.delete(path='/some')
    assert_valid_message(resp=resp, url=url, token=token, method='DELETE')


@responses.activate
def test_post_response(rest, url, token):
    add_response(responses.POST, url)

    resp = rest.post(path='/some', json={'bar': 'foo'})
    assert_valid_message(resp=resp, url=url, token=token, method='POST', body=True)


@responses.activate
def test_put_response(rest, url, token):
    add_response(responses.PUT, url)

    resp = rest.put(path='/some', json={'bar': 'foo'})
    assert_valid_message(resp=resp, url=url, token=token, method='PUT', body=True)


@responses.activate
def test_patch_response(rest, url, token):
    add_response(responses.PATCH, url)
    resp = rest.patch(path='/some', json={'bar': 'foo'})
    assert_valid_message(resp=resp, url=url, token=token, method='PATCH', body=True)


def add_response(method, url):
    responses.add(method, f'{url}/some.json', json=dict(message='what ever'), status=200)


def assert_valid_message(resp, url, method, token, body=False):
    assert resp.ok
    assert resp.status_code == 200
    assert resp.json()['message'] == 'what ever'
    request = responses.calls[0].request
    assert request.url == f'{url}/some.json?access_token={token}'
    assert request.path_url == f'/some.json?access_token={token}'
    if body:
        assert request.body.decode(encoding='utf-8') == '{"bar": "foo"}'
    assert request.method == method
