from tests.integration import asserts


def test_account_plans_list(api, account_plan):
    account_plans = api.account_plans.list()
    assert len(account_plans) >= 1


def test_account_plan_can_be_created(api, account_plan, account_plans_params):
    asserts.assert_resource(account_plan)
    asserts.assert_resource_params(account_plan, account_plans_params)

def test_account_plan_can_be_read(api, account_plan, account_plans_params):
    read = api.account_plans.read(account_plan.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_plans_params)


def test_account_plan_update(account_plan, account_plans_update_params):
    updated_account_plan = account_plan.update(params=account_plans_update_params)
    asserts.assert_resource(updated_account_plan)
    asserts.assert_resource_params(updated_account_plan, account_plans_update_params)

