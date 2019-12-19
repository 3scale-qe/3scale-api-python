def test_api_client(application, proxy):
    application.api_client_verify = False
    api_client = application.api_client()

    assert api_client is not None
    assert api_client._session.verify is False
    assert api_client.get("/get").status_code == 200
