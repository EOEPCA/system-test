import pytest
import os
import dotenv

from .fixtures.iam import *


@pytest.fixture(scope="session", autouse=True)
def load_env():
    # Load the 'base' env file
    dotenv.load_dotenv(override=True)
    # Load the specific env file
    target = os.getenv("target")
    if target:
        dotenv.load_dotenv(dotenv.find_dotenv(f".env.{target}"), override=True)
    return os.environ


@pytest.fixture(scope="session", autouse=True)
def DOMAIN(load_env):
    return load_env.get("DOMAIN")


@pytest.fixture(scope="session", autouse=True)
def KEYCLOAK(load_env):
    return load_env.get("KEYCLOAK")


@pytest.fixture(scope="session", autouse=True)
def SCHEME(load_env):
    return load_env.get("SCHEME")


@pytest.fixture(scope="session", autouse=True)
def REALM(load_env):
    return load_env.get("REALM")


@pytest.fixture(scope="session", autouse=True)
def TEST_USER(load_env):
    return load_env.get("TEST_USER")


@pytest.fixture(scope="session", autouse=True)
def TEST_PASSWORD(load_env):
    return load_env.get("TEST_PASSWORD")


@pytest.fixture(scope="session", autouse=True)
def ADMIN_CLIENT_ID(load_env):
    return load_env.get("ADMIN_CLIENT_ID")


@pytest.fixture(scope="session", autouse=True)
def ADMIN_CLIENT_SECRET(load_env):
    return load_env.get("ADMIN_CLIENT_SECRET")


@pytest.fixture(scope="session", autouse=True)
def OAPIP_CLIENT_ID(load_env):
    return load_env.get("OAPIP_CLIENT_ID")


@pytest.fixture(scope="session", autouse=True)
def OAPIP_CLIENT_SECRET(load_env):
    return load_env.get("OAPIP_CLIENT_SECRET")


@pytest.fixture(scope="session", autouse=True)
def EOAPI_CLIENT_ID(load_env):
    return load_env.get("EOAPI_CLIENT_ID")


@pytest.fixture(scope="session", autouse=True)
def EOAPI_CLIENT_SECRET(load_env):
    return load_env.get("EOAPI_CLIENT_SECRET")


@pytest.fixture(scope="session", autouse=True)
def EOAPI(load_env):
    return load_env.get("EOAPI")


@pytest.fixture(scope="session", autouse=True)
def MLOPS(load_env):
    return load_env.get("MLOPS")
