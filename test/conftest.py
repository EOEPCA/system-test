import pytest
import os
import dotenv

@pytest.fixture(scope='session', autouse=True)
def load_env():
  envname = os.getenv("envname", "")
  envfile = dotenv.find_dotenv((f".env.{envname}").rstrip("."))
  dotenv.load_dotenv(envfile)
  return os.environ

@pytest.fixture(scope='session', autouse=True)
def DOMAIN(load_env):
  return load_env.get("DOMAIN")

@pytest.fixture(scope='session', autouse=True)
def KEYCLOAK(load_env):
  return load_env.get("KEYCLOAK")

@pytest.fixture(scope='session', autouse=True)
def SCHEME(load_env):
  return load_env.get("SCHEME")

@pytest.fixture(scope='session', autouse=True)
def REALM(load_env):
  return load_env.get("REALM")

@pytest.fixture(scope='session', autouse=True)
def ADMIN_CLIENT_ID(load_env):
  return load_env.get("ADMIN_CLIENT_ID")

@pytest.fixture(scope='session', autouse=True)
def ADMIN_CLIENT_SECRET(load_env):
  return load_env.get("ADMIN_CLIENT_SECRET")

@pytest.fixture(scope='session', autouse=True)
def DUMMY_CLIENT_ID(load_env):
  return load_env.get("DUMMY_CLIENT_ID")

@pytest.fixture(scope='session', autouse=True)
def DUMMY_CLIENT_SECRET(load_env):
  return load_env.get("DUMMY_CLIENT_SECRET")

@pytest.fixture(scope='session', autouse=True)
def PORTAL_CLIENT_ID(load_env):
  return load_env.get("PORTAL_CLIENT_ID")

@pytest.fixture(scope='session', autouse=True)
def PORTAL_CLIENT_SECRET(load_env):
  return load_env.get("PORTAL_CLIENT_SECRET")
