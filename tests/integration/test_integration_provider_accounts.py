from tests.integration import asserts


def test_provider_user_can_be_created(provider_account, provider_account_params):
    asserts.assert_resource(provider_account)
    asserts.assert_resource_params(provider_account, provider_account_params)


def test_provider_account_list(api):
    accounts = api.provider_accounts.list()
    assert len(accounts) > 0


def test_provider_account_can_be_read(api, provider_account, provider_account_params):
    account = api.provider_accounts.read(provider_account.entity_id)
    asserts.assert_resource(account)
    asserts.assert_resource_params(account, provider_account_params)


def test_resource_role_change(provider_account):
    assert provider_account['role'] == 'member'
    updated = provider_account.set_role_admin()
    assert updated['role'] == 'admin'


def test_api_role_change(api, provider_account):
    assert provider_account['role'] == 'member'
    updated = api.provider_accounts.set_role_admin(provider_account.entity_id)
    assert updated['role'] == 'admin'
