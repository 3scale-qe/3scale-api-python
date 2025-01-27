import pytest
import backoff

from tests.integration.conftest import account
from threescale_api.errors import ApiClientError

from tests.integration import asserts

def test_should_create_service_subscription(account, service_subscription, service_subscription_params):

    account.service_subscriptions.create(params=service_subscription_params)
    resource = service_subscription.get(service_subscription_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(account, service_subscription_params, [param for param in service_subscription_params.keys() if param != 'id'])

def test_should_read_service_subscription(account, service_subscription, service_subscription_params):
    resource = account.service_subscriptions.get(params=service_subscription_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(resource, service_subscription_params, [param for param in service_subscription_params.keys() if param != 'id'])

#def test_should_update_service_subscription(account, service_subscription, service_subscription_params):
#    service_subscription_params['plan_id'] = 100
#    resource = account.service_subscriptions.update(service_subscription.entity_id, service_subscription_params)
#    asserts.assert_resource(resource)
#    asserts.assert_resource_params(resource, service_subscription_params, [param for param in service_subscription_params.keys() if param != 'id'])
#    resource_updated = account.service_subscription.read(params=service_subscription_params)
#    asserts.assert_resource(resource_updated)
#    asserts.assert_resource_params(resource_updated, service_subscription_params, [param for param in service_subscription_params.keys() if param != 'id'])

#def test_should_approve_service_subscription(account, service_subscription, service_subscription_params):
#    resource = account.service_subscriptions.approve_service_subscription(params=service_subscription_params)
#    asserts.assert_resource(resource)
#    read = account.service_subscriptions.read(service_subscription.entity_id)
#    asserts.assert_resource(read)

def test_list_service_subscriptions(account):
    resource = account.service_subscriptions.list()
    assert len(resource) >= 1

