from tests.integration import asserts
from .asserts import assert_resource, assert_resource_params


# Files
def test_file_list(api, cms_file):
    """ List all files. """
    assert len(list(api.cms_files.list())) >= 1


def test_file_can_be_created(cms_file_data, cms_file):
    """ Is file created properly? """
    assert_resource(cms_file)
    assert_resource_params(cms_file, cms_file_data)


def test_file_can_be_read(api, cms_file_data, cms_file):
    """ It is possible to get file by ID? """
    read = api.cms_files.read(cms_file.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, cms_file_data)


def test_file_can_be_read_by_name(api, cms_file_data, cms_file):
    """ It is possible to get file by name? """
    file_path = cms_file['path']
    read = api.cms_files[file_path]
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, cms_file_data)


def test_file_can_be_updated(cms_file_data, cms_file):
    """ Can be file object updated? """
    updated_path = cms_file['path'] = cms_file['path'] + 'up'
    cms_file.update()
    assert cms_file['path'] == updated_path
    updated = cms_file.read()
    assert updated['path'] == updated_path
    assert cms_file['path'] == updated_path


# Sections
# builtin

def test_builtin_section_list(api):
    """ List all sections. """
    assert len(list(api.cms_builtin_sections.list())) >= 1


def test_builtin_section_can_be_read(api):
    """ It is possible to get section by ID? """
    cms_section = next(api.cms_builtin_sections.list())
    read = api.cms_sections.read(cms_section.entity_id)
    asserts.assert_resource(read)

# user


def test_section_list(api, cms_section):
    """ List all sections. """
    assert len(list(api.cms_sections.list())) >= 1


def test_section_can_be_created(cms_section_params, cms_section):
    """ Is section created properly? """
    assert_resource(cms_section)
    assert_resource_params(cms_section, cms_section_params)


def test_section_can_be_read(api, cms_section_params, cms_section):
    """ It is possible to get section by ID? """
    read = api.cms_sections.read(cms_section.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, cms_section_params)


def test_section_can_be_updated(cms_section_params, cms_section):
    """ Can be section object updated? """
    updated_title = cms_section['title'] = cms_section['title'] + 'up'
    cms_section.update()
    assert cms_section['title'] == updated_title
    updated = cms_section.read()
    assert updated['title'] == updated_title
    assert cms_section['title'] == updated_title

# Partials
# builtin


def test_builtin_partials_list(api):
    """ List all sections. """
    assert len(list(api.cms_builtin_partials.list())) >= 1


def test_builtin_partial_can_be_read(api):
    """ It is possible to get partial by ID? """
    cms_partial = next(api.cms_builtin_partials.list())
    read = api.cms_builtin_partials.read(cms_partial.entity_id)
    asserts.assert_resource(read)

# user


def test_partial_list(api, cms_partial):
    """ List all user defined partials. """
    assert len(list(api.cms_partials.list())) >= 1


def test_partial_can_be_created(cms_partial_params, cms_partial):
    """ Is partial created properly? """
    assert_resource(cms_partial)
    assert_resource_params(cms_partial, cms_partial_params)


def test_partial_can_be_read(api, cms_partial_params, cms_partial):
    """ It is possible to get partial by ID? """
    read = api.cms_partials.read(cms_partial.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, cms_partial_params)


def test_partial_can_be_updated(cms_partial_params, cms_partial):
    """ Can be partial object updated? """
    updated_draft = cms_partial['draft'] = cms_partial['draft'] + 'up'
    cms_partial.update()
    assert cms_partial['draft'] == updated_draft
    updated = cms_partial.read()
    assert updated['draft'] == updated_draft
    assert cms_partial['draft'] == updated_draft

# # TODO pages, builtin_pages, layouts, template publishing
