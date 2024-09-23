import pytest
import requests

@pytest.fixture(scope="session")
def mlops_endpoint(SCHEME, MLOPS):
    return f"{SCHEME}://{MLOPS}"

@pytest.fixture(scope="session")
def mlops_config_api_endpoint(mlops_endpoint):
    return f"{mlops_endpoint}/api"

@pytest.fixture(scope="session")
def mlops_config(mlops_config_api_endpoint):
    config_endpoint = f"{mlops_config_api_endpoint}/config/"
    response =  requests.get(config_endpoint)
    assert response.ok, "SharingHub is down !"
    return response.json()
    
    