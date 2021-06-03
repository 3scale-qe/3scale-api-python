import pytest

from threescale_api.resources import InvoiceState
from .asserts import assert_resource, assert_resource_params


@pytest.fixture(scope="function")
def invoice_to_update(account, api):
    entity = api.invoices.create(dict(account_id=account['id']))
    yield entity
    entity.state_update(InvoiceState.cancelled)


def test_invoice_create(invoice):
    assert_resource(invoice)


def test_invoice_read(invoice, api):
    read = api.invoices.read(invoice.entity_id)
    assert_resource(read)
    assert_resource_params(read, invoice)


def test_invoice_list(invoice, api):
    invoices = api.invoices.list()
    assert len(invoices) >= 1


def test_invoice_update(invoice, api):
    assert invoice['state'] == 'open'
    update = api.invoices.update(invoice.entity_id, dict(friendly_id='1111-11111111'))
    assert update['friendly_id'] == '1111-11111111'
    read = api.invoices.read(invoice.entity_id)
    assert read['friendly_id'] == '1111-11111111'


def test_invoice_list_by_account(api, account, invoice):
    invoices = api.invoices.list_by_account(account.entity_id)
    assert len(invoices) == 1
    assert_resource(invoices[0])
    assert_resource_params(invoice, invoices[0])


def test_invoice_read_by_account(api, account, invoice):
    read = api.invoices.read_by_account(invoice.entity_id, account.entity_id)
    assert_resource(read)
    assert_resource_params(read, invoice)


def test_invoice_update_state(invoice_to_update, api):
    assert invoice_to_update['state'] == 'open'
    update = api.invoices.state_update(invoice_to_update.entity_id, InvoiceState.pending)
    assert update['state'] == 'pending'
    read = api.invoices.read(invoice_to_update.entity_id)
    assert read['state'] == 'pending'


def test_invoice_resource_update_state(invoice_to_update, api):
    assert invoice_to_update['state'] == 'open'
    update = invoice_to_update.state_update(InvoiceState.pending)
    assert update['state'] == 'pending'
    read = api.invoices.read(invoice_to_update.entity_id)
    assert read['state'] == 'pending'


def test_line_invoice_create(invoice_line):
    assert_resource(invoice_line)


def test_line_invoice_list(invoice, invoice_line):
    lines = invoice.line_items.list()
    assert len(lines) == 1
    assert_resource_params(invoice_line, lines[0])
