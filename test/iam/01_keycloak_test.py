import pytest
import requests

@pytest.mark.smoketest
def test_oidc_discovery(oidc_endpoint, token_endpoint, introspection_endpoint, userinfo_endpoint):
  assert oidc_endpoint is not None, "OIDC discovery"
  assert token_endpoint is not None, "Token endpoint discovery"
  assert introspection_endpoint is not None, "Introspection endpoint discovery"
  assert userinfo_endpoint is not None, "Userinfo endpoint discovery"

@pytest.mark.smoketest
def test_uma_discovery(uma_endpoint, resource_registration_endpoint, permission_endpoint, policy_endpoint):
  assert uma_endpoint is not None, "UMA discovery"
  assert resource_registration_endpoint is not None, "Resource Registration endpoint discovery"
  assert permission_endpoint is not None, "Permission endpoint discovery"
  assert policy_endpoint is not None, "Policy endpoint discovery"

@pytest.mark.acceptance
def test_authentication(eric_authenticate, eric_id_token, eric_access_token, eric_refresh_token):
  assert eric_authenticate is not None
  assert eric_id_token is not None
  assert eric_access_token is not None
  assert eric_refresh_token is not None

@pytest.mark.acceptance
def test_userinfo(userinfo_endpoint, eric_access_token):
  headers = {
    "Cache-Control": "no-cache",
    "Authorization": f"Bearer {eric_access_token}"
  }
  response = requests.get(userinfo_endpoint, headers=headers)
  assert response.ok, "Userinfo response status"
  assert response.json()["preferred_username"] == "eric", "Userinfo response content"
