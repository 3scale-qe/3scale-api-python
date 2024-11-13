from tests.integration import asserts


def test_accounts_list(api, account):
    accounts = api.accounts.list()
    assert len(accounts) >= 1


def test_account_can_be_created(api, account, account_params):
    asserts.assert_resource(account)
    asserts.assert_resource_params(account, account_params, ['org_name'])


def test_account_can_be_read(api, account, account_params):
    read = api.accounts.read(account.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params, ['org_name'])


def test_account_can_be_read_by_name(api, account, account_params):
    account_name = account['org_name']
    read = api.accounts[account_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params, ['org_name'])


def test_account_can_be_find_by_name(api, account_user, account_params):
    account2 = api.accounts.find(dict(username=account_user['username']))
    asserts.assert_resource(account2)
    asserts.assert_resource_params(account2, account_params, ['org_name'])


def test_account_update(api,account, update_account_params):
    updated_account = account.update(params=update_account_params)
    asserts.assert_resource(updated_account)
    asserts.assert_resource_params(updated_account, update_account_params)


def test_get_account_plan(account, account_get_plan_params):
    plan =  account.get_account_plan()
    asserts.assert_resource(plan)
    asserts.assert_resource_params(plan,account_get_plan_params, ['name'])


def test_users_list(api, account):
    assert len(account.users.list()) >= 1
