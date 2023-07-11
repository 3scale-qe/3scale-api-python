""" Test CMS API """

import pytest
from tests.integration import asserts
from threescale_api import errors
from .asserts import assert_resource, assert_resource_params


# Files
def test_file_list(api, cms_file):
    """ List all files. """
    assert len(api.cms_files.list()) >= 1


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
    updated_path = cms_file['path'] + 'up'
    cms_file['path'] = cms_file['path'] + 'up'
    # https://issues.redhat.com/browse/THREESCALE-9571
    for item in "created_at", "updated_at", "url", "title", "content_type":
        cms_file.pop(item)
    cms_file.update()
    assert cms_file['path'] == updated_path
    updated = cms_file.read()
    assert updated['path'] == updated_path
    assert cms_file['path'] == updated_path


# Sections


def test_section_list(api, cms_section):
    """ List all sections. """
    assert len(api.cms_sections.list()) >= 1


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
    updated_title = cms_section['title'] + 'up'
    cms_section['title'] = cms_section['title'] + 'up'
    # https://issues.redhat.com/browse/THREESCALE-9571
    for item in "created_at", "updated_at":
        cms_section.pop(item)
    cms_section.update()
    assert cms_section['title'] == updated_title
    updated = cms_section.read()
    assert updated['title'] == updated_title
    assert cms_section['title'] == updated_title


def test_builtin_section_delete(api):
    """It is not possible to delete section partial."""
    with pytest.raises(errors.ApiClientError) as exc_info:
        api.cms_sections.list()[0].delete()
    assert exc_info.value.code == 422


# Partials
# builtin


def test_builtin_partials_list(api):
    """ List all sections. """
    assert len(api.cms_builtin_partials.list()) >= 1


def test_builtin_partial_can_be_read(api):
    """ It is possible to get partial by ID? """
    cms_partial = api.cms_builtin_partials.list()[-1]
    read = api.cms_builtin_partials.read(cms_partial.entity_id)
    asserts.assert_resource(read)

def test_builtin_partial_delete(api):
    """It is not possible to delete builtin partial."""
    with pytest.raises(errors.ApiClientError) as exc_info:
        api.cms_builtin_partials.list()[0].delete()
    assert exc_info.value.code == 422

# user


def test_partial_list(api, cms_partial):
    """ List all user defined partials. """
    parts_list = api.cms_partials.list()
    assert len(parts_list) >= 1
    assert all('draft' in part.entity.keys() and 'published' in part.entity.keys()
                for part in parts_list)


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
    updated_draft = cms_partial['draft'] + 'up'
    cms_partial['draft'] = cms_partial['draft'] + 'up'
    # https://issues.redhat.com/browse/THREESCALE-9571
    for item in "created_at", "updated_at", "published":
        cms_partial.pop(item)
    cms_partial.update()
    assert cms_partial['draft'] == updated_draft
    updated = cms_partial.read()
    assert updated['draft'] == updated_draft
    assert cms_partial['draft'] == updated_draft


def test_partial_publish(cms_partial):
    """ Test publishing of partials. """
    assert cms_partial.entity.get('published', None) is None
    draft = cms_partial['draft']
    cms_partial = cms_partial.publish()
    assert cms_partial['draft'] == None
    assert draft == cms_partial['published']


# Pages
# builtin


def test_builtin_pages_list(api):
    """ List all sections. """
    assert len(api.cms_builtin_pages.list()) >= 1


def test_builtin_page_can_be_read(api):
    """ It is possible to get page by ID? """
    cms_page = api.cms_builtin_pages.list()[-1]
    read = api.cms_builtin_pages.read(cms_page.entity_id)
    asserts.assert_resource(read)


def test_builtin_page_delete(api):
    """It is not possible to delete builtin page."""
    with pytest.raises(errors.ApiClientError) as exc_info:
        api.cms_builtin_pages.list()[0].delete()
    assert exc_info.value.code == 422


# user


def test_page_list(api, cms_page):
    """ List all user defined pages. """
    assert len(api.cms_pages.list()) >= 1


def test_page_can_be_created(cms_page_params, cms_page):
    """ Is page created properly? """
    assert_resource(cms_page)
    assert_resource_params(cms_page, cms_page_params)


def test_page_can_be_read(api, cms_page_params, cms_page):
    """ It is possible to get page by ID? """
    read = api.cms_pages.read(cms_page.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, cms_page_params)


def test_page_can_be_updated(cms_page_params, cms_page):
    """ Can be page object updated? """
    updated_draft = cms_page['draft'] + 'up'
    cms_page['draft'] = cms_page['draft'] + 'up'
    # https://issues.redhat.com/browse/THREESCALE-9571
    for item in "created_at", "updated_at", "hidden", "published":
        cms_page.pop(item)
    cms_page.update()
    assert cms_page['draft'] == updated_draft
    updated = cms_page.read()
    assert updated['draft'] == updated_draft
    assert cms_page['draft'] == updated_draft


def test_page_publish(cms_page):
    """ Test publishing of pages. """
    assert cms_page.entity.get('published', None) is None
    draft = cms_page['draft']
    cms_page = cms_page.publish()
    assert draft == cms_page['published']


# Layouts


def test_layout_list(api, cms_layout):
    """ List all user defined layouts. """
    assert len(api.cms_layouts.list()) >= 1


def test_layout_can_be_created(cms_layout_params, cms_layout):
    """ Is layout created properly? """
    assert_resource(cms_layout)
    assert_resource_params(cms_layout, cms_layout_params)


def test_layout_can_be_read(api, cms_layout_params, cms_layout):
    """ It is possible to get layout by ID? """
    read = api.cms_layouts.read(cms_layout.entity_id)
    asserts.assert_resource(read)
    asserts.assert_resource_params(read, cms_layout_params)


def test_layout_can_be_updated(cms_layout_params, cms_layout):
    """ Can be layout object updated? """
    updated_draft = cms_layout['draft'] + 'up'
    cms_layout['draft'] = cms_layout['draft'] + 'up'
    # https://issues.redhat.com/browse/THREESCALE-9571
    for item in "created_at", "updated_at", "published":
        cms_layout.pop(item)
    cms_layout.update()
    assert cms_layout['draft'] == updated_draft
    updated = cms_layout.read()
    assert updated['draft'] == updated_draft
    assert cms_layout['draft'] == updated_draft


def test_layout_publish(cms_layout):
    """ Test publishing of layouts. """
    assert cms_layout.entity.get('published', None) is None
    draft = cms_layout['draft']
    cms_layout = cms_layout.publish()
    assert draft == cms_layout['published']

# filters
def test_section_filter(api, cms_section):
    """ Test section filtering """
    assert all(sec['parent_id'] == cms_section['parent_id']
                for sec in api.cms_sections.select_by(parent_id=cms_section['parent_id']))
    assert api.cms_sections.select_by(title=cms_section['title'])[0] == cms_section

def test_files_filter(api, cms_file, cms_section):
    """ Test files filtering """
    assert api.cms_files.select_by(section_id=cms_section['id'])[0] == cms_file
    assert api.cms_files.select_by(path=cms_file['path'])[0] == cms_file

# https://issues.redhat.com/browse/THREESCALE-9191?focusedId=22406548&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-22406548
def test_partial_filter(api, cms_partial, cms_section):
    """ Test partial filtering """
    assert api.cms_partials.select_by(section_id=cms_section['id']) == []
    assert api.cms_partials.select_by(system_name=cms_partial['system_name'])[0] == cms_partial

def test_layout_filter(api, cms_layout, cms_section):
    """ Test layout filtering """
    assert api.cms_layouts.select_by(section_id=cms_section['id']) == []
    assert api.cms_layouts.select_by(title=cms_layout['title'])[0] == cms_layout

def test_page_filter(api, cms_section, cms_page):
    """ Test page filtering """
    assert api.cms_pages.select_by(section_id=cms_section['id'])[0] == cms_page
    assert api.cms_pages.select_by(title=cms_page['title'])[0] == cms_page
