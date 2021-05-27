from tests.integration import asserts


def test_provider_user_can_be_created(provider_account_user, provider_account_params):
    asserts.assert_resource(provider_account_user)
    asserts.assert_resource_params(provider_account_user, provider_account_params)


def test_provider_user_list(api):
    accounts = api.provider_accounts.list()
    assert len(accounts) > 0


def test_provider_user_can_be_read(api, provider_account_user, provider_account_params):
    account = api.provider_account_users.read(provider_account_user.entity_id)
    asserts.assert_resource(account)
    asserts.assert_resource_params(account, provider_account_params)


def test_resource_role_change(provider_account_user):
    assert provider_account_user['role'] == 'member'
    updated = provider_account_user.set_role_admin()
    assert updated['role'] == 'admin'


def test_api_role_change(api, provider_account_user):
    assert provider_account_user['role'] == 'member'
    updated = api.provider_account_users.set_role_admin(provider_account_user.entity_id)
    assert updated['role'] == 'admin'


def test_api_read_permissions(api, provider_account_user):
    provider_account_user.set_role_admin()
    response = api.provider_account_users.permissions_read(provider_account_user.entity_id)
    permissions = response['permissions']
    assert 'portal' in permissions['allowed_sections']


def test_resource_read_permissions(provider_account_user):
    provider_account_user.set_role_admin()
    response = provider_account_user.permissions_read()
    permissions = response['permissions']
    assert 'portal' in permissions['allowed_sections']


def test_resource_update_permissions(service, provider_account_user):
    provider_account_user.set_role_member()
    response = provider_account_user.permissions_update()
    permissions = response['permissions']
    assert 'portal' not in permissions['allowed_sections']
    assert service['id'] not in permissions['allowed_service_ids']

    response = provider_account_user.permissions_update(
        allowed_services=[service['id']], allowed_sections=['portal'])
    permissions = response['permissions']
    assert 'portal' in permissions['allowed_sections']
    assert service['id'] in permissions['allowed_service_ids']
