def test_read_by_name_account(account, api):
    """Test for read_by_name when entity has entity_name"""
    acc = api.accounts.read_by_name(account.entity_name)
    assert acc == account


def test_read_by_name_account_plan(account_plan, api):
    """Test for read_by_name when entity hasn't entity_name"""
    acc_plan = api.account_plans.read_by_name(account_plan.entity_name)
    assert acc_plan == account_plan


def test_read_by_name_application(application, account, api):
    """Test for read_by_name when entity has entity_name"""
    app = account.applications.read_by_name(application.entity_name)
    assert app == application
