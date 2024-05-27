import random
import string
import secrets
import pytest

from tests.integration import asserts


@pytest.fixture(scope='module')
def update_application_params():
    suffix = secrets.token_urlsafe(8)
    name = f"updated-{suffix}"
    return dict(name=name, description=name)


def test_application_can_be_created(application, application_params):
    asserts.assert_resource(application)
    asserts.assert_resource_params(application, application_params)


def test_application_list(account, application):
    applications = account.applications.list()
    assert len(applications) > 0


def test_application_update(application, update_application_params):
    updated_application = application.update(params=update_application_params)
    asserts.assert_resource(updated_application)
    asserts.assert_resource_params(updated_application, update_application_params)


def test_application_key_can_be_created(app_key, app_key_params):
    asserts.assert_resource(app_key)
    asserts.assert_resource_params(app_key, app_key_params)


def test_application_key_list(application, app_key):
    keys = application.keys.list()
    assert len(keys) > 0

def test_application_update_userkey(application):
    new_key = "".join(random.choices(string.ascii_letters + string.digits + "-_.", k=100))
    updated_application = application.update(params={"user_key": new_key})
    asserts.assert_resource(updated_application)
    assert updated_application["user_key"] == new_key
