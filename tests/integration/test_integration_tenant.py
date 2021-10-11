from datetime import date
import backoff

from threescale_api import client


def test_trigger_billing(master_api, custom_tenant):
    assert master_api.tenants.trigger_billing(custom_tenant, date.today().isoformat())


def test_trigger_billing_account(master_api, custom_tenant, account_params):
    admin_url = custom_tenant["signup"]["account"]["admin_base_url"]
    token = custom_tenant["signup"]["access_token"]["value"]
    tenant_api = client.ThreeScaleClient(admin_url, token, ssl_verify=False)
    wait_for_tenant_initialise(tenant_api)

    account = None
    while not account:
        accounts_list = tenant_api.accounts.list()
        if len(accounts_list) >= 1:
            account = tenant_api.accounts.list()[0].entity_id

    assert master_api.tenants.trigger_billing_account(custom_tenant, account, date.today().isoformat())


@backoff.on_predicate(backoff.fibo, lambda x: (not x.accounts.exists()) or len(x.accounts.list()) < 1 or
                      (not x.account_plans.exists()) or len(x.account_plans.list()) < 1,
                      max_tries=8, jitter=None)
def wait_for_tenant_initialise(tenant):
    """
    Retries until an account plan is created. When that objects exists, tenant is ready.
    When fetching account plans without previous check if they have been created
    503 error can be returned
    """
    return tenant

