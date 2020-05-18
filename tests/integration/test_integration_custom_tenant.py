from .asserts import assert_resource


def test_3scale_master_url_is_set(master_api, master_url, master_token):
    assert master_url
    assert master_token
    assert master_api.url


def test_tenant_can_be_created(custom_tenant, tenant_params):
    assert_resource(custom_tenant)
    assert custom_tenant.entity["signup"]['account']['admin_domain']
    assert custom_tenant.entity["signup"]["access_token"]["value"]
