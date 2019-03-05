import pytest
import secrets

from tests.integration import asserts


@pytest.fixture(scope='module')
def update_params():
    suffix = secrets.token_urlsafe(8)
    return dict(name=f"updated-{suffix}", cost_per_month='12.0', setup_fee='50.0')


def test_application_plan_can_be_created(api, application_plan_params, application_plan):
    asserts.assert_resource(application_plan)
    asserts.assert_resource_params(application_plan, application_plan_params)


def test_application_plans_list(service):
    app_plans = service.app_plans.list()
    assert len(app_plans) == 1


def test_application_plan_update(application_plan, update_params):
    updated_app_plan = application_plan.update(params=update_params)
    asserts.assert_resource(updated_app_plan)
    asserts.assert_resource_params(updated_app_plan, update_params)
