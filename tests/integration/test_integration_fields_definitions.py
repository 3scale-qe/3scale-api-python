from .asserts import assert_resource, assert_resource_params


def test_fields_definitions_create(api, fields_definition, fields_definitions_params):
    assert_resource(fields_definition)
    assert_resource_params(fields_definition, fields_definitions_params)


def test_fields_definitions_list(api):
    assert len(api.fields_definitions.list()) > 0


def test_fields_definitions_read(api):
    default_field = api.fields_definitions.list()[0]
    read = api.fields_definitions.read(default_field.entity_id)
    assert_resource(read)
    assert default_field['target'] == read['target']
    assert default_field['position'] == read['position']


def test_fields_definitions_update(api, fields_definition):
    update_params = dict(target="Cinstance", label="something_else",
                         hidden="true", read_only="true", position=1)
    updated = fields_definition.update(update_params)
    assert_resource_params(updated, update_params)


def test_fields_definitions_delete(api, fields_definitions_params):
    fields_definitions_params.update(dict(name="something_else"))
    created = api.fields_definitions.create(fields_definitions_params)
    assert api.fields_definitions.delete(created.entity_id)
