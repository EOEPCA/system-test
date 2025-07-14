import pytest
import requests


@pytest.fixture
def iam_headers():
    return {"Cache-Control": "no-cache"}


@pytest.fixture
def iam_auth_headers(iam_headers, test_user_access_token):
    return {
        **iam_headers,
        "Authorization": f"Bearer {test_user_access_token}",
    }


@pytest.mark.acceptance
def test_introspect(
    introspection_endpoint,
    iam_headers,
    OAPIP_CLIENT_ID,
    OAPIP_CLIENT_SECRET,
    test_user_access_token,
):
    data = {
        "client_id": OAPIP_CLIENT_ID,
        "client_secret": OAPIP_CLIENT_SECRET,
        "token": test_user_access_token,
    }
    response = requests.post(introspection_endpoint, headers=iam_headers, data=data)
    assert response.ok, "Token introspection"
    assert response.json()["active"], "Token is active"


@pytest.mark.acceptance
def test_authorisation_decision(
    token_endpoint, TEST_USER, iam_auth_headers, OAPIP_CLIENT_ID
):
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
        "audience": OAPIP_CLIENT_ID,
        "permission_resource_format": "uri",
        "permission": f"/{TEST_USER}/*",
        "response_mode": "decision",
    }
    response = requests.post(token_endpoint, headers=iam_auth_headers, data=data)
    assert response.ok, "Authorisation decision"
    assert response.json()["result"], "Authorisation decision ALLOWED"


@pytest.mark.acceptance
def test_authorisation_permissions(
    token_endpoint, TEST_USER, iam_auth_headers, OAPIP_CLIENT_ID
):
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
        "audience": OAPIP_CLIENT_ID,
        "permission_resource_format": "uri",
        "permission": f"/{TEST_USER}/*",
    }
    response = requests.post(token_endpoint, headers=iam_auth_headers, data=data)
    assert response.ok, "Authorisation permissions"
    assert response.json()["access_token"] is not None


@pytest.mark.acceptance
def test_authorisation_path_matching(
    token_endpoint, TEST_USER, iam_auth_headers, OAPIP_CLIENT_ID
):
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
        "audience": OAPIP_CLIENT_ID,
        "permission_resource_format": "uri",
        "permission": f"/{TEST_USER}",
        "permission_resource_matching_uri": "true",
        "response_mode": "decision",
    }
    response = requests.post(token_endpoint, headers=iam_auth_headers, data=data)
    assert response.ok, "Authorisation decision path matching"
    assert response.json()["result"], "Authorisation decision path matching ALLOWED"


@pytest.mark.acceptance
def test_unauthorised(token_endpoint, TEST_USER, iam_headers, OAPIP_CLIENT_ID):
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
        "audience": OAPIP_CLIENT_ID,
        "permission_resource_format": "uri",
        "permission": f"/{TEST_USER}",
        "permission_resource_matching_uri": "true",
    }
    response = requests.post(token_endpoint, headers=iam_headers, data=data)
    assert response.status_code == 401, "Authorisation decision UNAUTHORIZED"
    assert (
        response.json()["error_description"]
        == "Invalid client or Invalid client credentials"
    )
