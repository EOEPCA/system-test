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
def oapip_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('oapip_test')
    output_notebook = temp_output_dir / 'oapip-output.ipynb'
    executed_notebook = temp_output_dir / 'oapip-executed.ipynb'
    log_output_file = temp_output_dir / 'oapip_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'oapip'

    # platform_domain, oapip_user, S3 stage-out config etc. are left to the
    # notebook's own defaults, derived from `load_eoepca_state()`.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'oapip.ipynb'

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
@pytest.mark.oapip
def test_authentication(oapip_test_results):
    assert oapip_test_results['authentication']['status'] == 'PASS', \
        f"Authentication failed: {oapip_test_results['authentication']['message']}"

@pytest.mark.smoketest
@pytest.mark.oapip
def test_api_endpoints_healthy(oapip_test_results):
    assert oapip_test_results['api_endpoints_healthy']['status'] == 'PASS', \
        f"API endpoint health check failed: {oapip_test_results['api_endpoints_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.oapip
def test_list_processes(oapip_test_results):
    assert oapip_test_results['list_processes']['status'] == 'PASS', \
        f"Processes listing failed: {oapip_test_results['list_processes']['message']}"

@pytest.mark.smoketest
@pytest.mark.oapip
def test_echo_process_execution(oapip_test_results):
    assert oapip_test_results['echo_process_execution']['status'] == 'PASS', \
        f"Built-in echo process execution failed: {oapip_test_results['echo_process_execution']['message']}"

@pytest.mark.smoketest
@pytest.mark.oapip
def test_deploy_custom_process(oapip_test_results):
    assert oapip_test_results['deploy_custom_process']['status'] == 'PASS', \
        f"Custom Application Package deployment failed: {oapip_test_results['deploy_custom_process']['message']}"

@pytest.mark.smoketest
@pytest.mark.oapip
def test_custom_process_execution(oapip_test_results):
    assert oapip_test_results['custom_process_execution']['status'] == 'PASS', \
        f"Custom process execution failed: {oapip_test_results['custom_process_execution']['message']}"

@pytest.mark.smoketest
@pytest.mark.oapip
def test_custom_process_output_verified(oapip_test_results):
    assert oapip_test_results['custom_process_output_verified']['status'] == 'PASS', \
        f"Custom process output verification failed: {oapip_test_results['custom_process_output_verified']['message']}"

@pytest.mark.smoketest
@pytest.mark.oapip
def test_undeploy_custom_process(oapip_test_results):
    assert oapip_test_results['undeploy_custom_process']['status'] == 'PASS', \
        f"Process undeployment failed: {oapip_test_results['undeploy_custom_process']['message']}"
