import pytest

from threescale_api.resources import ApplicationPlan, Limits


@pytest.fixture()
def limit_client(application_plan, metric) -> Limits:
    return application_plan.limits(metric)


@pytest.fixture()
def limits(metric, application_plan: ApplicationPlan):
    params = dict(period='minute', value=10)
    application_plan.limits(metric).create(params)
    return application_plan.limits(metric).list()


def test_create_limit(limits):
    assert limits is not None
    limit = limits[0]
    assert limit['period'] == 'minute'
    assert limit['value'] == 10
