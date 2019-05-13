from typing import List

import requests

import threescale_api.defaults


def assert_resource(resource: threescale_api.defaults.DefaultResource):
    assert resource is not None
    assert resource.entity_id is not None
    assert resource.entity is not None


def assert_errors_contains(resource: threescale_api.defaults.DefaultClient, fields: List[str]):
    errors = resource['errors']
    assert errors is not None
    for field in fields:
        assert field in errors


def assert_resource_params(obj: threescale_api.defaults.DefaultResource, params: dict, allowed=None):
    for (key, val) in params.items():
        if allowed is not None and key in allowed:
            assert obj[key] == val, f"Resource value for key \"{key}\" should be correct."
            assert obj.entity[key] == val, "Entity value for key \"{key}\" should be correct."


def assert_http_ok(response: requests.Response):
    assert response.status_code == 200
