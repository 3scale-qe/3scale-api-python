import os

import pytest

import threescale

from dotenv import load_dotenv
load_dotenv()


@pytest.fixture(scope='session')
def url() -> str:
    return os.getenv('THREESCALE_PROVIDER_URL')


@pytest.fixture(scope='session')
def token() -> str:
    return os.getenv('THREESCALE_PROVIDER_TOKEN')


@pytest.fixture(scope='session')
def master_url() -> str:
    return os.getenv('THREESCALE_MASTER_URL')


@pytest.fixture(scope='session')
def master_token() -> str:
    return os.getenv('THREESCALE_MASTER_TOKEN')


@pytest.fixture(scope='session')
def api(url, token) -> threescale.ThreeScaleClient:
    return threescale.ThreeScaleClient(url=url, token=token)


@pytest.fixture(scope='session')
def master_api(master_url, master_token) -> threescale.ThreeScaleClient:
    return threescale.ThreeScaleClient(url=master_url, token=master_token)
