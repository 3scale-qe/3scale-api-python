# 3scale REST API client in Python

3Scale REST API client in a wrapper over the 3scale API.

[![lint & smoke](https://github.com/3scale-qe/3scale-api-python/actions/workflows/lint-and-smoke.yml/badge.svg)](https://github.com/3scale-qe/3scale-api-python/actions)

## Installing

Install and update using pip:

```bash
pip install 3scale-api
```

Or as a dependency using the pipenv

```bash
pipenv install 3scale-api
```

## Usage

Client supports basic CRUD operations and it using the official 3scale API.

The API can be found at `<https://yourdomain-admin.3scale.net>/p/admin/api_docs`

Basic usage of the client:


```python
from threescale_api import ThreeScaleClient, resources
from typing import List

client = ThreeScaleClient(url="myaccount.3scale.net", token="secret_token", ssl_verify=True)

# Get list of APIs/Services or any other resource
services: List[resources.Service] = client.services.list()

# Get service by it's name
test_service: resources.Service = client.services["test_service"] # or use: client.services.read_by_name(system_name)

# Get service by it's id
test_service: resources.Service = client.services[12345] # or use client.services.read(id)

# To get raw JSON response - you can use the fetch method - it takes the service id
raw_json: dict = client.services.fetch(12345)

# To create a new service (or any other resource), parameters are the same as you would provide by the documentation
new_service: resources.Service = client.services.create(system_name='my_testing_service', name="My Testing service")

# In order to update service you can either
client.services[123456].update(param="new_value")
# or
service: resources.Service = client.services[123456]
service['param'] = 'new_value'
service.update()

# To get a proxy config you can use
proxy: resources.Proxy = client.services['test_service'].proxy.read()

# To update the proxy you can either
proxy: resources.Proxy = client.services['test_service'].proxy.update(parameter_to_update='update')
# or
proxy_instance = client.services['test_service'].proxy.read()
proxy_instance['param'] = 'new_value'
proxy_instance.update()

# On the service you can access the:
service: resources.Service = client.services[123456]
service.proxy           # The PROXY client
service.mapping_rules   # mapping rules client
service.metrics         # metrics
service.app_plans       # application plans

# The proxy supports:
proxy = service.proxy.read()
proxy.promote(version=1, from_env="sandbox", to_env="production") # The promote operation
proxy.mapping_rules # The mapping rules
proxy.configs       # proxy configurations client
proxy.policies      # Policies defined for the API
```

## Run the Tests

To run the tests you need to have installed development dependencies:
```bash
pipenv install --dev
```

and then run the `pytest`:

```bash
pipenv run pytest -v
```

### Integration tests configuration

To run the integration tests you need to set these env variables:
```
THREESCALE_PROVIDER_URL='https://example-admin.3scale.net'
THREESCALE_PROVIDER_TOKEN='<test-token>'

# OPTIONAL:
THREESCALE_MASTER_URL='https://master.3scale.net'
THREESCALE_MASTER_TOKEN='<test-master-token>'
```


