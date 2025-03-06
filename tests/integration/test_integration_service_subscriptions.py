
from tests.integration import asserts

def test_list_service_subscriptions(account):
    resource = account.service_subscriptions.list()
    assert len(resource) >= 1

def test_create_service_subscription(service_subscription, service_subscription_params):
    asserts.assert_resource(service_subscription)
    asserts.assert_resource_params(service_subscription, service_subscription_params)

def test_read_service_subscription(account, service_subscription, service_subscription_params):
    resource = account.service_subscriptions.read(service_subscription.entity_id)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(service_subscription,service_subscription_params)

def test_change_plan_service_subscription(account, account_plan, service_plan,
                                          service_subscription):
    asserts.assert_resource(account)
    asserts.assert_resource(account_plan)
    asserts.assert_resource(service_plan)
    account.service_subscriptions.change_plan(service_subscription.entity_id,
                                                         service_plan.entity_id)

def test_approve_service_subscription(account, service_subscription, service_plan):
    asserts.assert_resource(service_subscription)
    asserts.assert_resource(account)
    asserts.assert_resource(service_plan)
    svc_subs_id = service_subscription.entity_id
    resource = account.service_subscriptions.approve(svc_subs_id)
    asserts.assert_resource(resource)
