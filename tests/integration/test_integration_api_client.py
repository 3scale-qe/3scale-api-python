from threescale_api.utils import HttpClient


def test_api_client(application, proxy):
    application.api_client_verify = False
    api_client = application.api_client()

    assert api_client is not None
    assert api_client._session.verify is False
    assert api_client.get("/get").status_code == 200


def always_no_ssl_client(application, endpoint, session, verify):
    client = HttpClient(application, endpoint, session, verify)
    client._session.verify = False
    return client


def test_api_client_replacement(application, proxy):
    application.api_client_verify = True
    application._client_factory = always_no_ssl_client
    api_client = application.api_client()

    assert api_client is not None
    assert api_client._session.verify is False
    assert api_client.get("/get").status_code == 200
