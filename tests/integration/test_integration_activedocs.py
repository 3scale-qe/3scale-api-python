from tests.integration import asserts
from .asserts import assert_resource, assert_resource_params

def test_active_docs_fetch(active_doc):
    ac = active_doc.client.fetch(int(active_doc['id']))
    assert ac
    assert ac['id'] == active_doc['id']
