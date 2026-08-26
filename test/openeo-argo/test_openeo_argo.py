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
def openeo_argo_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('openeo_argo_test')
    output_notebook = temp_output_dir / 'openeo-argo-output.ipynb'
    executed_notebook = temp_output_dir / 'openeo-argo-executed.ipynb'
    log_output_file = temp_output_dir / 'openeo_argo_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'openeo-argo'

    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'openeo-argo.ipynb'

    try:
        pm.execute_notebook(
            input_path=str(input_notebook_path),
            output_path=str(output_notebook),
            parameters=params,
            log_output=True,
            prepare_only=True,
            cwd=str(notebook_repo_path)
        )

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
@pytest.mark.openeo_argo
def test_authentication(openeo_argo_test_results):
    assert openeo_argo_test_results['authentication']['status'] == 'PASS', \
        f"Authentication failed: {openeo_argo_test_results['authentication']['message']}"

@pytest.mark.smoketest
@pytest.mark.openeo_argo
def test_collection_exists(openeo_argo_test_results):
    assert openeo_argo_test_results['collection_exists']['status'] == 'PASS', \
        f"Collection check failed: {openeo_argo_test_results['collection_exists']['message']}"

@pytest.mark.smoketest
@pytest.mark.openeo_argo
def test_list_processes(openeo_argo_test_results):
    assert openeo_argo_test_results['list_processes']['status'] == 'PASS', \
        f"Process listing failed: {openeo_argo_test_results['list_processes']['message']}"

@pytest.mark.smoketest
@pytest.mark.openeo_argo
def test_batch_job_completed(openeo_argo_test_results):
    assert openeo_argo_test_results['batch_job_completed']['status'] == 'PASS', \
        f"Batch job did not complete: {openeo_argo_test_results['batch_job_completed']['message']}"

@pytest.mark.smoketest
@pytest.mark.openeo_argo
def test_ndvi_result_downloaded(openeo_argo_test_results):
    assert openeo_argo_test_results['ndvi_result_downloaded']['status'] == 'PASS', \
        f"NDVI result check failed: {openeo_argo_test_results['ndvi_result_downloaded']['message']}"
