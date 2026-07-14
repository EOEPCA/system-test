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
def data_access_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('data_access_test')
    output_notebook = temp_output_dir / 'data-access-output.ipynb'
    executed_notebook = temp_output_dir / 'data-access-executed.ipynb'
    log_output_file = temp_output_dir / 'data-access_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'data-access'

    # platform_domain, username, sample_collection_id etc. are left to the
    # notebook's own defaults, derived from `load_eoepca_state()`.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'data-access.ipynb'

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
@pytest.mark.data_access
def test_service_health(data_access_test_results):
    assert data_access_test_results['service_health']['status'] == 'PASS', \
        f"Service health check failed: {data_access_test_results['service_health']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_collection_exists(data_access_test_results):
    assert data_access_test_results['collection_exists']['status'] == 'PASS', \
        f"Sample collection missing: {data_access_test_results['collection_exists']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_stac_search(data_access_test_results):
    assert data_access_test_results['stac_search']['status'] == 'PASS', \
        f"STAC search failed: {data_access_test_results['stac_search']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_raster_preview(data_access_test_results):
    assert data_access_test_results['raster_preview']['status'] == 'PASS', \
        f"Raster preview failed: {data_access_test_results['raster_preview']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_vector_collections(data_access_test_results):
    assert data_access_test_results['vector_collections']['status'] == 'PASS', \
        f"Vector collections listing failed: {data_access_test_results['vector_collections']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_openeo_capabilities(data_access_test_results):
    assert data_access_test_results['openeo_capabilities']['status'] == 'PASS', \
        f"openEO capabilities check failed: {data_access_test_results['openeo_capabilities']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_unauthenticated_write_rejected(data_access_test_results):
    assert data_access_test_results['unauthenticated_write_rejected']['status'] == 'PASS', \
        f"Unauthenticated write check failed: {data_access_test_results['unauthenticated_write_rejected']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_owned_collection_write(data_access_test_results):
    assert data_access_test_results['owned_collection_write']['status'] == 'PASS', \
        f"Owned collection write failed: {data_access_test_results['owned_collection_write']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_unauthorized_write_rejected(data_access_test_results):
    assert data_access_test_results['unauthorized_write_rejected']['status'] == 'PASS', \
        f"Unauthorized write check failed: {data_access_test_results['unauthorized_write_rejected']['message']}"

@pytest.mark.smoketest
@pytest.mark.data_access
def test_private_collection_visibility(data_access_test_results):
    assert data_access_test_results['private_collection_visibility']['status'] == 'PASS', \
        f"Private collection visibility check failed: {data_access_test_results['private_collection_visibility']['message']}"
