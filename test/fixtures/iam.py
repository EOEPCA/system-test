import pytest
import requests

# -------------------------------------------------------------------------------
# OIDC
# -------------------------------------------------------------------------------


@pytest.fixture(scope="package")
def oidc_endpoint(SCHEME, KEYCLOAK, REALM):
    url = f"{SCHEME}://{KEYCLOAK}/realms/{REALM}/.well-known/openid-configuration"
    response = requests.get(url)
    assert response.ok, "OIDC discovery"
    return response.json()


@pytest.fixture(scope="package")
def token_endpoint(oidc_endpoint):
    if "token_endpoint" in oidc_endpoint:
        return oidc_endpoint["token_endpoint"]
    return None


@pytest.fixture(scope="package")
def introspection_endpoint(oidc_endpoint):
    if "introspection_endpoint" in oidc_endpoint:
        return oidc_endpoint["introspection_endpoint"]
    return None


@pytest.fixture(scope="package")
def userinfo_endpoint(oidc_endpoint):
    if "userinfo_endpoint" in oidc_endpoint:
        return oidc_endpoint["userinfo_endpoint"]
    return None


# -------------------------------------------------------------------------------
# UMA
# -------------------------------------------------------------------------------


@pytest.fixture(scope="package")
def uma_endpoint(SCHEME, KEYCLOAK, REALM):
    url = f"{SCHEME}://{KEYCLOAK}/realms/{REALM}/.well-known/uma2-configuration"
    response = requests.get(url)
    assert response.ok, "UMA discovery"
    return response.json()


@pytest.fixture(scope="package")
def resource_registration_endpoint(uma_endpoint):
    if "resource_registration_endpoint" in uma_endpoint:
        return uma_endpoint["resource_registration_endpoint"]
    return None


@pytest.fixture(scope="package")
def permission_endpoint(uma_endpoint):
    if "permission_endpoint" in uma_endpoint:
        return uma_endpoint["permission_endpoint"]
    return None


@pytest.fixture(scope="package")
def policy_endpoint(uma_endpoint):
    if "policy_endpoint" in uma_endpoint:
        return uma_endpoint["policy_endpoint"]
    return None


# -------------------------------------------------------------------------------
# Test user authentication
# -------------------------------------------------------------------------------


# default user credentials - can be overridden by module fixtures
@pytest.fixture(scope="function")
def user_credentials(TEST_USER, TEST_PASSWORD):
    return TEST_USER, TEST_PASSWORD


# default client credentials - can be overridden by module fixtures
@pytest.fixture(scope="function")
def client_credentials(ADMIN_CLIENT_ID, ADMIN_CLIENT_SECRET):
    return ADMIN_CLIENT_ID, ADMIN_CLIENT_SECRET


@pytest.fixture(scope="function")
def test_user_authenticate(token_endpoint, user_credentials, client_credentials):
    TEST_USER, TEST_PASSWORD = user_credentials
    CLIENT_ID, CLIENT_SECRET = client_credentials

    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "scope": "openid profile email",
        "grant_type": "password",
        "username": TEST_USER,
        "password": TEST_PASSWORD,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_endpoint, headers=headers, data=data)
    assert response.ok, "User authenticate"
    return response.json()


@pytest.fixture(scope="function")
def test_user_id_token(test_user_authenticate):
    if "id_token" in test_user_authenticate:
        return test_user_authenticate["id_token"]
    return None


@pytest.fixture(scope="function")
def test_user_access_token(test_user_authenticate):
    if "access_token" in test_user_authenticate:
        return test_user_authenticate["access_token"]
    return None


@pytest.fixture(scope="function")
def test_user_refresh_token(test_user_authenticate):
    if "refresh_token" in test_user_authenticate:
        return test_user_authenticate["refresh_token"]
    return None
