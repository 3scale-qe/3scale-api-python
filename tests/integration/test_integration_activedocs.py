from tests.integration import asserts


def test_active_docs_can_be_created(active_doc, active_docs_params):
    asserts.assert_resource(active_doc)
    asserts.assert_resource_params(active_doc, active_docs_params)


def test_active_docs_fetch(active_doc):
    ac = active_doc.client.fetch(int(active_doc['id']))
    assert ac
    assert ac['id'] == active_doc['id']


def test_active_docs_list(api, active_doc):
    active_docs = api.active_docs.list()
    assert len(active_docs) >= 1


def test_active_docs_update(active_doc, active_docs_update_params):
    updated_active_doc = active_doc.update(params=active_docs_update_params)
    asserts.assert_resource(updated_active_doc)
    asserts.assert_resource_params(updated_active_doc, active_docs_update_params)
