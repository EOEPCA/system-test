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
def resource_registration_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('resource_registration_test')
    output_notebook = temp_output_dir / 'resource-registration-output.ipynb'
    executed_notebook = temp_output_dir / 'resource-registration-executed.ipynb'
    log_output_file = temp_output_dir / 'resource-registration_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'resource-registration'

    # platform_domain, operaton credentials etc. are left to the notebook's own
    # defaults, derived from `load_eoepca_state()`.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'resource-registration.ipynb'

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
@pytest.mark.resource_registration
def test_registration_api_endpoints_healthy(resource_registration_test_results):
    assert resource_registration_test_results['registration_api_endpoints_healthy']['status'] == 'PASS', \
        f"Registration API endpoint health check failed: {resource_registration_test_results['registration_api_endpoints_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_registration
def test_processes_list(resource_registration_test_results):
    assert resource_registration_test_results['processes_list']['status'] == 'PASS', \
        f"Processes listing failed: {resource_registration_test_results['processes_list']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_registration
def test_hello_world_execution(resource_registration_test_results):
    assert resource_registration_test_results['hello_world_execution']['status'] == 'PASS', \
        f"hello-world process execution failed: {resource_registration_test_results['hello_world_execution']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_registration
def test_stac_collection_registration(resource_registration_test_results):
    assert resource_registration_test_results['stac_collection_registration']['status'] == 'PASS', \
        f"STAC collection registration failed: {resource_registration_test_results['stac_collection_registration']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_registration
def test_operaton_engine_healthy(resource_registration_test_results):
    assert resource_registration_test_results['operaton_engine_healthy']['status'] == 'PASS', \
        f"Operaton engine health check failed: {resource_registration_test_results['operaton_engine_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_registration
def test_harvester_workflows_deployed(resource_registration_test_results):
    assert resource_registration_test_results['harvester_workflows_deployed']['status'] == 'PASS', \
        f"Harvester workflow deployment failed: {resource_registration_test_results['harvester_workflows_deployed']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_registration
def test_stac_harvest_started(resource_registration_test_results):
    assert resource_registration_test_results['stac_harvest_started']['status'] == 'PASS', \
        f"STAC harvest process start failed: {resource_registration_test_results['stac_harvest_started']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_registration
def test_stac_harvest_completed(resource_registration_test_results):
    # Known to currently fail: workflows/stac.bpmn's multi-instance loop reads ${collections},
    # but worker.stac.tasks.StacCatalogHandler sets stac_collection_source instead - a
    # variable-name mismatch in the upstream EOEPCA/registration-harvester repo, not this
    # deployment.
    assert resource_registration_test_results['stac_harvest_completed']['status'] == 'PASS', \
        f"STAC harvest did not complete: {resource_registration_test_results['stac_harvest_completed']['message']}"
