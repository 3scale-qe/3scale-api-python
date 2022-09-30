import pytest

from tests.integration import asserts
from threescale_api.errors import ApiClientError
from threescale_api.resources import InvoiceState


@pytest.fixture(scope="function")
def pending_invoice(account, api, invoice_line_params):
    invoice = api.invoices.create(dict(account_id=account['id']))
    invoice.line_items.create(invoice_line_params)
    invoice.state_update(InvoiceState.PENDING)
    yield invoice
    invoice = invoice.read()
    if invoice["state"] != InvoiceState.PAID.value:
        invoice.state_update(InvoiceState.CANCELLED)


@pytest.fixture(scope="function")
def fake_credit_card(account):
    fake_params = dict(credit_card_token="fake",
                       credit_card_expiration_year=1,
                       credit_card_expiration_month=1,
                       credit_card_partial_number="fake",
                       billing_address_name="fake",
                       billing_address_address="fake",
                       billing_address_city="fake",
                       billing_address_country="fake")
    response = account.credit_card_set(fake_params)
    yield response
    account.credit_card_delete()


def test_charge_unbound_credit_card(pending_invoice):
    transactions_old = pending_invoice.payment_transactions.list()

    with pytest.raises(ApiClientError, match="Failed to charge the credit card") as error:
        pending_invoice = pending_invoice.charge()
    assert error.value.code == 422

    transactions_new = pending_invoice.payment_transactions.list()
    assert len(transactions_old) == len(transactions_new)


def test_charge_bound_credit_card_success(pending_invoice, credit_card, invoice_line_params):
    transactions_old = pending_invoice.payment_transactions.list()

    pending_invoice = pending_invoice.charge()
    asserts.assert_resource(pending_invoice)

    transactions_new = pending_invoice.payment_transactions.list()
    assert len(transactions_old) == len(transactions_new) - 1

    transaction = transactions_new[-1]
    assert transaction["success"] is True
    assert "Transaction approved" in transaction["message"]
    assert transaction["amount"] == invoice_line_params["cost"]


def test_charge_bound_credit_card_fail(account, pending_invoice, fake_credit_card, invoice_line_params):
    transactions_old = pending_invoice.payment_transactions.list()

    with pytest.raises(ApiClientError, match="Failed to charge the credit card") as error:
        pending_invoice = pending_invoice.charge()
    assert error.value.code == 422

    transactions_new = pending_invoice.payment_transactions.list()
    assert len(transactions_old) == len(transactions_new) - 1

    transaction = transactions_new[-1]
    assert transaction["success"] is False
    assert "No such customer" in transaction["message"]
    assert transaction["amount"] == invoice_line_params["cost"]
