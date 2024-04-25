import pytest
import requests

@pytest.fixture
def iam_headers():
  return {
    "Cache-Control": "no-cache"
  }

@pytest.fixture
def iam_auth_headers(iam_headers, eric_access_token):
  return {
    **iam_headers,
    "Authorization": f"Bearer {eric_access_token}",
  }

def test_introspect(introspection_endpoint, iam_headers, DUMMY_CLIENT_ID, DUMMY_CLIENT_SECRET, eric_access_token):
  data = {
    "client_id": DUMMY_CLIENT_ID,
    "client_secret": DUMMY_CLIENT_SECRET,
    "token": eric_access_token
  }
  response = requests.post(introspection_endpoint, headers=iam_headers, data=data)
  assert response.ok, "Token introspection"
  assert response.json()["active"], "Token is active"

def test_authorisation_decision(token_endpoint, iam_auth_headers, eric_access_token, DUMMY_CLIENT_ID):
  data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
    "audience": DUMMY_CLIENT_ID,
    "permission_resource_format": "uri",
    "permission": "/eric/*",
    "response_mode": "decision"
  }
  response = requests.post(token_endpoint, headers=iam_auth_headers, data=data)
  assert response.ok, "Authorisation decision"
  assert response.json()["result"], "Authorisation decision ALLOWED"

def test_authorisation_permissions(token_endpoint, iam_auth_headers, eric_access_token, DUMMY_CLIENT_ID):
  data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
    "audience": DUMMY_CLIENT_ID,
    "permission_resource_format": "uri",
    "permission": "/eric/*"
  }
  response = requests.post(token_endpoint, headers=iam_auth_headers, data=data)
  assert response.ok, "Authorisation permissions"
  assert response.json()["access_token"] is not None

def test_authorisation_path_matching(token_endpoint, iam_auth_headers, eric_access_token, DUMMY_CLIENT_ID):
  data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
    "audience": DUMMY_CLIENT_ID,
    "permission_resource_format": "uri",
    "permission": "/eric",
    "permission_resource_matching_uri": "true",
    "response_mode": "decision"
  }
  response = requests.post(token_endpoint, headers=iam_auth_headers, data=data)
  assert response.ok, "Authorisation decision path matching"
  assert response.json()["result"], "Authorisation decision path matching ALLOWED"

def test_unauthorised(token_endpoint, iam_auth_headers, eric_access_token, DUMMY_CLIENT_ID):
  data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
    "audience": DUMMY_CLIENT_ID,
    "permission_resource_format": "uri",
    "permission": "/bob",
    "permission_resource_matching_uri": "true"
  }
  response = requests.post(token_endpoint, headers=iam_auth_headers, data=data)
  assert response.status_code == 403, "Authorisation decision FORBIDDEN"
  assert response.json()["error_description"] == "not_authorized"
