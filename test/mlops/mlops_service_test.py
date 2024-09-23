import pytest
import requests

@pytest.mark.smoketest
def test_gitlab_deployment(mlops_config):
    gitlab_config = mlops_config["gitlab"]
    assert isinstance(gitlab_config, dict)
    assert gitlab_config.get("url")
    response = requests.get(gitlab_config.get("url"))
    assert response.ok, "GitLab deployment is down!"

@pytest.mark.smoketest
def test_mlflow_deployment(mlops_config):
    mlflow_config = mlops_config["mlflow"]
    assert isinstance(mlflow_config, dict)
    assert mlflow_config.get("url")
    response = requests.get(mlflow_config.get("url"))
    assert response.status_code == 401, "ML Trainer deployment is down!"

@pytest.mark.acceptance
def test_storage_deployment(mlops_config):
    assert mlops_config["store"], "DVC S3 is not configured"