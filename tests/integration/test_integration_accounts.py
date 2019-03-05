from tests.integration import asserts


def test_accounts_list(api):
    services = api.accounts.list()
    assert len(services) > 1


def test_service_can_be_created(api, account, account_params):
    asserts.assert_resource(account)
    asserts.assert_resource_params(account, account_params)
