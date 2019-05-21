import pytest

from threescale_api.resources import ApplicationPlan


@pytest.fixture()
def pricing_rules(metric, application_plan: ApplicationPlan):
    params = dict(min=10, max=100, cost_per_unit=20)
    application_plan.pricing_rules(metric).create(params)
    return application_plan.pricing_rules(metric).list()


def test_create_pricing_rule(pricing_rules):
    assert pricing_rules is not None
    rule = pricing_rules[0]
    assert rule['max'] == 100
    assert rule['min'] == 10
    assert rule['cost_per_unit'] == '20.0'
