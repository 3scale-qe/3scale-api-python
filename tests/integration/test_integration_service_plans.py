

from tests.integration import asserts

def test_list_service_plans(service):
    resource = service.service_plans.list()
    assert len(resource) >= 1

def test_check_service_plan_creation(service_plan, service_plan_params):
    asserts.assert_resource(service_plan)
    asserts.assert_resource_params(service_plan, service_plan_params)
    assert service_plan.exists()

def test_read_service_plans(service, service_plan, service_plan_params):
    asserts.assert_resource(service_plan)
    resource = service.service_plans.read(service_plan.entity_id)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(service_plan,service_plan_params)

def test_update_service_plans(service, service_plan, service_plan_params):
    asserts.assert_resource(service_plan)
    service_plan['state'] = 'publish'
    service_plan['approval_required'] = True
    resource = service.service_plans.update(service_plan.entity_id, service_plan_params)
    asserts.assert_resource(resource)
    asserts.assert_resource_params(service_plan, service_plan_params)

def test_set_default_service_plan(service_plan, service_plan_params):
    asserts.assert_resource(service_plan)
    resource = service_plan.set_default()
    asserts.assert_resource(resource)
    asserts.assert_resource_params(service_plan, service_plan_params)
