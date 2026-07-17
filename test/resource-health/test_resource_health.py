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
def resource_health_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('resource_health_test')
    output_notebook = temp_output_dir / 'health-output.ipynb'
    executed_notebook = temp_output_dir / 'health-executed.ipynb'
    log_output_file = temp_output_dir / 'resource_health_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'resource-health'

    # resource_health_domain, resource_health_enable_oidc etc. are left to the
    # notebook's own defaults, derived from `load_eoepca_state()` - the
    # Keycloak client is CONFIDENTIAL with a password grant, so no
    # interactive auth flow override is needed here.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'health.ipynb'

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
@pytest.mark.resource_health
def test_endpoints_healthy(resource_health_test_results):
    assert resource_health_test_results['endpoints_healthy']['status'] == 'PASS', \
        f"Endpoint health check failed: {resource_health_test_results['endpoints_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_health
def test_create_check(resource_health_test_results):
    assert resource_health_test_results['create_check']['status'] == 'PASS', \
        f"Health check creation failed: {resource_health_test_results['create_check']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_health
def test_check_appears_in_list(resource_health_test_results):
    assert resource_health_test_results['check_appears_in_list']['status'] == 'PASS', \
        f"Health check not listed after creation: {resource_health_test_results['check_appears_in_list']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_health
def test_trigger_check_run(resource_health_test_results):
    assert resource_health_test_results['trigger_check_run']['status'] == 'PASS', \
        f"Triggering a manual run failed: {resource_health_test_results['trigger_check_run']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_health
def test_check_result_recorded(resource_health_test_results):
    assert resource_health_test_results['check_result_recorded']['status'] == 'PASS', \
        f"Check result not recorded in telemetry: {resource_health_test_results['check_result_recorded']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_health
def test_delete_check(resource_health_test_results):
    assert resource_health_test_results['delete_check']['status'] == 'PASS', \
        f"Health check deletion failed: {resource_health_test_results['delete_check']['message']}"
