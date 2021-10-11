from .asserts import assert_resource, assert_resource_params
from datetime import date

from ..test_3scale_api_client import _create_client


def test_create_tenant(custom_tenant, tenant_params):
    assert_resource(custom_tenant)
    assert_resource_params(custom_tenant, tenant_params)


def test_update_tenant(master_api, custom_tenant, tenant_params):
    params = dict(from_email="anything@anything.invalid", support_email="anything2@anything.invalid",
                  finance_support_email="anything3@anything.invalid", site_access_code="123456")
    updated = master_api.tenants.update(custom_tenant.entity_id, params=params)
    for key in params.keys():
        assert updated[key] == params[key]


def test_delete_tenant(master_api, tenant_params):
    created = master_api.tenants.create(tenant_params)
    created.delete()
    deleted = master_api.tenants.read(created.entity_id)
    assert deleted['state'] == "scheduled_for_deletion"


def test_show_tenant(master_api, custom_tenant):
    showed = master_api.tenants.read(custom_tenant.entity_id)
    assert_resource(showed)
    assert showed.entity_id == custom_tenant.entity_id


def test_show_by_name_tenant(master_api, custom_tenant):
    # because of lack of "tenant list" read_by_name doesnt work, after its added this can be uncommented

    # showed = master_api.tenants.read_by_name(custom_tenant.entity_name)
    # assert_resource(showed)
    # assert showed.entity_id == custom_tenant.entity_id

    pass


def test_trigger_billing(master_api, custom_tenant):
    returned = master_api.tenants.trigger_billing(custom_tenant, date.today().isoformat())
    assert_resource(returned)
    #todo


def test_trigger_billing_account(master_api, custom_tenant):
    #todo
    tenant_api = _create_client(custom_tenant.url, custom_tenant['token'])


    returned = master_api.tenants.trigger_billing_account(custom_tenant)
