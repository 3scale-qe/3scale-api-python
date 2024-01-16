from datetime import date, timedelta
from random import randint

import backoff
import pytest


# Some of the tests can fail randomly because of tenant not being 100% ready, be warned

@pytest.fixture()
def next_day() -> str:
    return (date.today() + timedelta(days=1)).isoformat()


@pytest.fixture()
def paid_account(service_params, account_params, account_plans_params, application_plan_params):
    def _paid_account(api):
        """
        Creates new account with payed app plan on default service.
        No need for deletion as all is happening on temporary tenant.
        """
        service = api.services.list()[0]

        account_params.update(org_name=f"test-{randint(1,10000)}", username=f"test-{randint(1,10000)}")
        account = api.accounts.create(account_params)

        application_plan_params.update(name=f"test-{randint(1,10000)}", setup_fee="5", cost_per_month="5")
        app_plan = service.app_plans.create(params=application_plan_params)

        application_params = dict(name=f"test-{randint(1,10000)}", description="desc", plan_id=app_plan.entity_id)
        account.applications.create(params=application_params)

        return account
    return _paid_account


@backoff.on_predicate(backoff.fibo, lambda x: x == 0, max_tries=8, jitter=None)
def count_invoice(api, account):
    # creating the invoice takes some time
    return len(api.invoices.list_by_account(account))


def test_trigger_billing(master_api, custom_tenant, paid_account, next_day, ssl_verify):
    api = custom_tenant.admin_api(ssl_verify=ssl_verify, wait=True)
    account = paid_account(api)
    assert master_api.tenants.trigger_billing(custom_tenant, next_day)
    assert count_invoice(api, account) == 1


def test_trigger_billing_resource(custom_tenant, paid_account, next_day, ssl_verify):
    api = custom_tenant.admin_api(ssl_verify=ssl_verify, wait=True)
    account = paid_account(api)
    assert custom_tenant.trigger_billing(next_day)
    assert count_invoice(api, account) == 1


def test_trigger_billing_account(master_api, custom_tenant, paid_account, next_day, ssl_verify):
    api = custom_tenant.admin_api(ssl_verify=ssl_verify, wait=True)
    account = paid_account(api)
    assert master_api.tenants.trigger_billing_account(custom_tenant, account, next_day)
    assert count_invoice(api, account) == 1


def test_trigger_billing_account_resource(custom_tenant, paid_account, next_day, ssl_verify):
    api = custom_tenant.admin_api(ssl_verify=ssl_verify, wait=True)
    account = paid_account(api)
    assert custom_tenant.trigger_billing_account(account, next_day)
    assert count_invoice(api, account) == 1
