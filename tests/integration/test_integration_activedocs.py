from unittest import skipIf

import pytest

from tests.integration import asserts
from .asserts import assert_resource, assert_resource_params
from .conftest import active_docs_params, get_suffix


@pytest.fixture(scope='module')
def active_docs_update_body():
    return """
    {"swagger":"2.0","info":{"version":"1.0.1","title":"Test"},"paths":{"/test":{"get":{"operationId":"Test",
    "parameters":[],"responses":{"400":{"description":"bad input parameters"}}}}},"definitions":{}}
    """

@pytest.fixture(scope='module')
def active_docs_update_params(active_docs_update_body):
    suffix = get_suffix()
    name = f"updated-{suffix}"
    return dict(name=name, body=active_docs_update_body)


def test_active_docs_fetch(active_doc):
    ac = active_doc.client.fetch(int(active_doc['id']))
    assert ac
    assert ac['id'] == active_doc['id']


def test_active_docs_update(active_doc,active_docs_update_params):
    updated_active_doc = active_doc.update(params=active_docs_update_params)
    asserts.assert_resource(updated_active_doc)
    asserts.assert_resource_params(updated_active_doc, active_docs_update_params)
