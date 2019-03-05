from tests.integration import asserts


def test_accounts_list(api):
    services = api.accounts.list()
    assert len(services) > 1


def test_account_can_be_created(api, account, account_params):
    asserts.assert_resource(account)
    asserts.assert_resource_params(account, account_params)


def test_account_can_be_read(api, account, account_params):
    read = api.accounts.read(account.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)


def test_account_can_be_read_by_name(api, account, account_params):
    account_name = account['org_name']
    read = api.accounts[account_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)
