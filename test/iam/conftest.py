import pytest
import requests

#-------------------------------------------------------------------------------
# OIDC
#-------------------------------------------------------------------------------

@pytest.fixture(scope='package')
def oidc_endpoint(SCHEME, KEYCLOAK, REALM):
  url = f"{SCHEME}://{KEYCLOAK}/realms/{REALM}/.well-known/openid-configuration"
  response = requests.get(url)
  assert response.ok, "OIDC discovery"
  return response.json()

@pytest.fixture(scope='package')
def token_endpoint(oidc_endpoint):
  if "token_endpoint" in oidc_endpoint:
    return oidc_endpoint["token_endpoint"]
  return None

@pytest.fixture(scope='package')
def introspection_endpoint(oidc_endpoint):
  if "introspection_endpoint" in oidc_endpoint:
    return oidc_endpoint["introspection_endpoint"]
  return None

@pytest.fixture(scope='package')
def userinfo_endpoint(oidc_endpoint):
  if "userinfo_endpoint" in oidc_endpoint:
    return oidc_endpoint["userinfo_endpoint"]
  return None

#-------------------------------------------------------------------------------
# UMA
#-------------------------------------------------------------------------------

@pytest.fixture(scope='package')
def uma_endpoint(SCHEME, KEYCLOAK, REALM):
  url = f"{SCHEME}://{KEYCLOAK}/realms/{REALM}/.well-known/uma2-configuration"
  response = requests.get(url)
  assert response.ok, "UMA discovery"
  return response.json()

@pytest.fixture(scope='package')
def resource_registration_endpoint(uma_endpoint):
  if "resource_registration_endpoint" in uma_endpoint:
    return uma_endpoint["resource_registration_endpoint"]
  return None

@pytest.fixture(scope='package')
def permission_endpoint(uma_endpoint):
  if "permission_endpoint" in uma_endpoint:
    return uma_endpoint["permission_endpoint"]
  return None

@pytest.fixture(scope='package')
def policy_endpoint(uma_endpoint):
  if "policy_endpoint" in uma_endpoint:
    return uma_endpoint["policy_endpoint"]
  return None

#-------------------------------------------------------------------------------
# eric authentication
#-------------------------------------------------------------------------------

@pytest.fixture(scope='function')
def eric_authenticate(token_endpoint):
  headers = {
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded"
  }
  data = {
    "scope": "openid profile email",
    "grant_type": "password",
    "username": "eric",
    "password": "changeme",
    "client_id": "eoepca-portal",
    "client_secret": "changeme"
  }
  response = requests.post(token_endpoint, headers=headers, data=data)
  assert response.ok, "Eric authenticate"
  return response.json()

@pytest.fixture(scope='function')
def eric_id_token(eric_authenticate):
  if "id_token" in eric_authenticate:
    return eric_authenticate["id_token"]
  return None

@pytest.fixture(scope='function')
def eric_refresh_token(eric_authenticate):
  if "refresh_token" in eric_authenticate:
    return eric_authenticate["refresh_token"]
  return None

@pytest.fixture(scope='function')
def eric_access_token(eric_authenticate):
  if "access_token" in eric_authenticate:
    return eric_authenticate["access_token"]
  return None
