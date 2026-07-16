import json
import os
import pytest
import papermill as pm
import sys
from pathlib import Path

# Add this repo to Python path so we can import the wrapper and executor
sys.path.append(str(Path(__file__).resolve().parent.parent))

from test.run_notebook import execute_wrapped_notebook

@pytest.fixture(scope='module')
def mlops_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('mlops_test')
    output_notebook = temp_output_dir / 'mlops-output.ipynb'
    executed_notebook = temp_output_dir / 'mlops-executed.ipynb'
    log_output_file = temp_output_dir / 'mlops_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'mlops'

    # project_name, MLOPS_OIDC_ENABLED etc. are left to the notebook's own defaults,
    # derived from `load_eoepca_state()` - GitLab's OIDC sign-in is scripted directly
    # (no interactive login involved), so no authentication_method override is needed.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'mlops.ipynb'

    try:
        # Prepare the notebook with Papermill (injecting parameters but not executing yet)
        pm.execute_notebook(
            input_path=str(input_notebook_path),
            output_path=str(output_notebook),
            parameters=params,
            log_output=True,
            prepare_only=True,
            cwd=str(notebook_repo_path)
        )

        # Execute the notebook with wrapping logic
        execute_wrapped_notebook(
            input_path=output_notebook,
            output_path=executed_notebook,
            execution_path=notebook_repo_path
        )

    except Exception as e:
        pytest.fail(f"Notebook execution failed: {e}")

    with open(str(log_output_file), 'r') as f:
        test_results = json.load(f)

    return test_results

@pytest.mark.smoketest
@pytest.mark.mlops
def test_services_healthy(mlops_test_results):
    assert mlops_test_results['services_healthy']['status'] == 'PASS', \
        f"Service health check failed: {mlops_test_results['services_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_stac_catalogue_browsable(mlops_test_results):
    assert mlops_test_results['stac_catalogue_browsable']['status'] == 'PASS', \
        f"STAC catalogue browsing failed: {mlops_test_results['stac_catalogue_browsable']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_gitlab_oidc_login(mlops_test_results):
    assert mlops_test_results['gitlab_oidc_login']['status'] == 'PASS', \
        f"GitLab OIDC login failed: {mlops_test_results['gitlab_oidc_login']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_gitlab_project_ready(mlops_test_results):
    assert mlops_test_results['gitlab_project_ready']['status'] == 'PASS', \
        f"GitLab project setup failed: {mlops_test_results['gitlab_project_ready']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_sharinghub_discovery(mlops_test_results):
    assert mlops_test_results['sharinghub_discovery']['status'] == 'PASS', \
        f"SharingHub discovery failed: {mlops_test_results['sharinghub_discovery']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_mlflow_tracking_token(mlops_test_results):
    assert mlops_test_results['mlflow_tracking_token']['status'] == 'PASS', \
        f"MLflow tracking token setup failed: {mlops_test_results['mlflow_tracking_token']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_mlflow_experiment_run(mlops_test_results):
    assert mlops_test_results['mlflow_experiment_run']['status'] == 'PASS', \
        f"MLflow experiment run failed: {mlops_test_results['mlflow_experiment_run']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_mlflow_run_validation(mlops_test_results):
    assert mlops_test_results['mlflow_run_validation']['status'] == 'PASS', \
        f"MLflow run validation failed: {mlops_test_results['mlflow_run_validation']['message']}"

@pytest.mark.smoketest
@pytest.mark.mlops
def test_mlflow_artifact_storage(mlops_test_results):
    assert mlops_test_results['mlflow_artifact_storage']['status'] == 'PASS', \
        f"MLflow artifact storage validation failed: {mlops_test_results['mlflow_artifact_storage']['message']}"
