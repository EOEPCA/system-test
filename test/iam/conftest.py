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
# eric authentication
# -------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def user_authenticate(
    token_endpoint, TEST_USER, TEST_PASSWORD, ADMIN_CLIENT_ID, ADMIN_CLIENT_SECRET
):
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "scope": "openid profile email",
        "grant_type": "password",
        "username": TEST_USER,
        "password": TEST_PASSWORD,
        "client_id": ADMIN_CLIENT_ID,
        "client_secret": ADMIN_CLIENT_SECRET,
    }
    response = requests.post(token_endpoint, headers=headers, data=data)
    assert response.ok, "User authenticate"
    return response.json()


@pytest.fixture(scope="function")
def user_id_token(user_authenticate):
    if "id_token" in user_authenticate:
        return user_authenticate["id_token"]
    return None


@pytest.fixture(scope="function")
def user_access_token(user_authenticate):
    if "access_token" in user_authenticate:
        return user_authenticate["access_token"]
    return None


@pytest.fixture(scope="function")
def user_refresh_token(user_authenticate):
    if "refresh_token" in user_authenticate:
        return user_authenticate["refresh_token"]
    return None
