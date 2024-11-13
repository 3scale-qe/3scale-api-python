from  tests.integration import asserts
from tests.integration.conftest import account


def test_account_user_can_be_created(account_user, account_user_params):
    asserts.assert_resource(account_user)
    asserts.assert_resource_params(account_user, account_user_params)


def test_account_users_list(api,account, account_user):
    users = account.users.list()
    assert len(users) > 1


def test_account_users_get_by_id(account, account_user, account_user_params):
    account_user = account.users.read(account_user['id'])
    asserts.assert_resource(account_user)
    asserts.assert_resource_params(account_user, account_user_params)


def test_account_user_can_be_updated(account_user, account_user_update_params):
    updated_user = account_user.update(account_user_update_params)
    asserts.assert_resource(updated_user)
    asserts.assert_resource_params(updated_user, account_user_update_params)


def test_account_user_change_status(account_user):
    assert account_user['state'] == 'pending'
    updated_account_user = account_user.activate()
    assert updated_account_user['state'] == 'active'

    updated_account_user = account_user.suspend()
    assert updated_account_user['state'] == 'suspended'

    updated_account_user = account_user.un_suspend()
    assert updated_account_user['state'] == 'active'


def test_account_user_change_role(account_user):
    assert account_user['role'] == 'member'

    updated_account_user = account_user.set_as_admin()
    assert  updated_account_user['role'] == 'admin'

    updated_account_user = account_user.set_as_member()
    assert updated_account_user['role'] == 'member'
