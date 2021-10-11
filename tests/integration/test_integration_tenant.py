from datetime import date


def test_trigger_billing(master_api, custom_tenant):
    assert master_api.tenants.trigger_billing(custom_tenant, date.today().isoformat())


def test_trigger_billing_resource(custom_tenant):
    assert custom_tenant.trigger_billing(date.today().isoformat())


def test_trigger_billing_account(master_api, custom_tenant):
    # this test can sometimes fail randomly because of tenant not being 100% ready
    account = custom_tenant.admin_api(wait=True).accounts.list()[0]
    assert master_api.tenants.trigger_billing_account(custom_tenant, account, date.today().isoformat())


def test_trigger_billing_account_resource(custom_tenant):
    # this test can sometimes fail randomly because of tenant not being 100% ready
    account = custom_tenant.admin_api(wait=True).accounts.list()[0]
    assert custom_tenant.trigger_billing_account(account, date.today().isoformat())
