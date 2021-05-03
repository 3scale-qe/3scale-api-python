from . import asserts

def test_access_tokens_list(api, access_token):
    access_tokens = api.access_tokens.list()
    assert len(access_tokens) >= 1


def test_access_token_can_be_created(api, access_token, access_token_params):
    asserts.assert_resource(access_token)
    asserts.assert_resource_params(access_token, access_token_params)


def test_access_token_can_be_read(api, access_token, access_token_params):
    read = api.access_tokens.read(access_token.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, access_token_params)


def test_access_token_can_be_read_by_name(api, access_token, access_token_params):
    access_token_name = access_token["name"]
    read = api.access_tokens[access_token_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, access_token_params)
