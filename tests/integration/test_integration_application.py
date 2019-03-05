import pytest
import secrets

from tests.integration import asserts


@pytest.fixture(scope='module')
def update_application_params():
    suffix = secrets.token_urlsafe(8)
    name = f"updated-{suffix}"
    return dict(name=name, description=name)


def test_application_can_be_created(application, application_params):
    asserts.assert_resource(application)
    asserts.assert_resource_params(application, application_params)


def test_application_list(account):
    applications = account.applications.list()
    assert len(applications) > 0


def test_application_update(application, update_application_params):
    updated_application = application.update(params=update_application_params)
    asserts.assert_resource(updated_application)
    asserts.assert_resource_params(updated_application, update_application_params)
