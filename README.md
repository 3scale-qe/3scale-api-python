# 3scale REST API client in Python

3Scale REST API client in a wrapper over the 3scale API.

## Installing

Install and update using pip:

```bash
pip install 3scale-api
```

Or as a dependency using the pipenv

```bash
pipenv install 3scale-api
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
