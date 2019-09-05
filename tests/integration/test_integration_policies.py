def test_policies_insert_append(proxy):
    #test_append
    policies = proxy.policies.list()
    policy_1 = {
                "name": "logging",
                "configuration": {},
                "version": "builtin",
                "enabled": True
            }
    proxy.policies.append(policy_1)
    policies["policies_config"].append(policy_1)       
    updated_policies = proxy.policies.list()
    assert policies["policies_config"] == updated_policies["policies_config"]
    #test_insert
    policy_2 = {
                "name": "echo",
                "configuration": {},
                "version": "builtin",
                "enabled": True
            }
    proxy.policies.insert(1, policy_2)
    updated_policies["policies_config"].insert(1, policy_2)
    newly_updated_policies = proxy.policies.list()
    assert updated_policies["policies_config"] == newly_updated_policies["policies_config"]