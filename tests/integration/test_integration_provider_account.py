from .asserts import assert_resource
from .conftest import get_suffix


def test_provider_account_read(provider_account):
    assert_resource(provider_account)


def test_provider_account_update(provider_account, api):
    update_access_code = get_suffix()
    api.provider_accounts.update(dict(site_access_code=update_access_code))
    update = api.provider_accounts.fetch()
    assert update['site_access_code'] == update_access_code


def test_provider_account_resource_update(provider_account, api):
    update_access_code = get_suffix()
    provider_account.update(dict(site_access_code=update_access_code))
    assert provider_account['site_access_code'] == update_access_code
    update = api.provider_accounts.fetch()
    assert update['site_access_code'] == update_access_code
