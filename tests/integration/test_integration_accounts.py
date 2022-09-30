from tests.integration import asserts


def test_accounts_list(api):
    services = api.accounts.list()
    assert len(services) >= 1


def test_account_can_be_created(api, account, account_params):
    asserts.assert_resource(account)
    asserts.assert_resource_params(account, account_params)


def test_account_can_be_read(api, account, account_params):
    read = api.accounts.read(account.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)


def test_account_can_be_read_by_name(api, account, account_params):
    account_name = account['org_name']
    read = api.accounts[account_name]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, account_params)


def test_add_credit_card(account, credit_card, api_credit_card_params):
    asserts.assert_resource(account)
    asserts.assert_http_ok(credit_card)

    account = account.read()
    assert account["credit_card_stored"] is True
    assert account["credit_card_partial_number"] == api_credit_card_params["credit_card_partial_number"]
    exp_year = api_credit_card_params['credit_card_expiration_year']
    exp_month = api_credit_card_params['credit_card_expiration_month']
    assert account["credit_card_expires_on"] == f"{exp_year:04d}-{exp_month:02d}-01"


def test_delete_credit_card(account, credit_card):
    asserts.assert_resource(account)
    asserts.assert_http_ok(credit_card)

    account.read()
    assert account["credit_card_stored"] is True

    response = account.credit_card_delete()
    asserts.assert_http_ok(response)

    account.read()
    assert account["credit_card_stored"] is False
    assert account.get("credit_card_partial_number") is None
    assert account.get("credit_card_expires_on") is None
