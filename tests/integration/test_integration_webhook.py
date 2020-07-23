import json


def test_webhooks(webhook):
    # Test for Keys webhooks
    expected = {"url": "https://example.com",
                "active": "true",
                "provider_actions": "true",
                "application_key_created_on": "true",
                "application_key_deleted_on": "true",
                "application_key_updated_on": "true"
                }
    request = webhook.setup("Keys", "https://example.com")
    data = json.loads(request.request.body.decode(encoding='UTF-8'))
    assert data == expected

    # Test for Users webhooks
    expected = {"url": "https://example.com",
                "active": "true",
                "provider_actions": "true",
                "user_created_on": "true",
                "user_updated_on": "true",
                "user_deleted_on": "true"
                }
    request = webhook.setup("Users", "https://example.com")
    data = json.loads(request.request.body.decode(encoding='UTF-8'))
    assert data == expected

    # Test for Applications webhooks
    expected = {"url": "https://example.com",
                "active": "true",
                "provider_actions": "true",
                "application_created_on": "true",
                "application_updated_on": "true",
                "application_suspended_on": "true",
                "application_plan_changed_on": "true",
                "application_user_key_updated_on": "true",
                "application_deleted_on": "true"
                }
    request = webhook.setup("Applications", "https://example.com")
    data = json.loads(request.request.body.decode(encoding='UTF-8'))
    assert data == expected

    # Test for Accounts webhooks
    expected = {"url": "https://example.com",
                "active": "true",
                "provider_actions": "true",
                "account_created_on": "true",
                "account_updated_on": "true",
                "account_deleted_on": "true",
                "account_plan_changed_on": "true"
                }
    request = webhook.setup("Accounts", "https://example.com")
    data = json.loads(request.request.body.decode(encoding='UTF-8'))
    assert data == expected

    # Test for clear webhooks
    expected = {"url": "",
                "active": "false",
                "provider_actions": "false",
                "account_created_on": "false",
                "account_updated_on": "false",
                "account_deleted_on": "false",
                "user_created_on": "false",
                "user_updated_on": "false",
                "user_deleted_on": "false",
                "application_created_on": "false",
                "application_updated_on": "false",
                "application_deleted_on": "false",
                "account_plan_changed_on": "false",
                "application_plan_changed_on": "false",
                "application_user_key_updated_on": "false",
                "application_key_created_on": "false",
                "application_key_deleted_on": "false",
                "application_suspended_on": "false",
                "application_key_updated_on": "false",
                }

    request = webhook.clear()
    data = json.loads(request.request.body.decode(encoding='UTF-8'))
    assert data == expected
