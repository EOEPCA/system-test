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
def openeo_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('openeo_test')
    output_notebook = temp_output_dir / 'openeo-output.ipynb'
    executed_notebook = temp_output_dir / 'openeo-executed.ipynb'
    log_output_file = temp_output_dir / 'openeo_log.json'

    notebook_repo_path = Path(os.getenv("NOTEBOOK_PATH", "/home/eouser/code/deployment-guide/notebooks/examples"))

    params = {
        'openeo_backend': 'openeo.notebook-test.develop.eoepca.org',
        'authentication_method': 'authorization-code',
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'openeo.ipynb'

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
def test_authentication(openeo_test_results):
    assert openeo_test_results['authentication']['status'] == 'PASS', \
        f"Authentication failed: {openeo_test_results['authentication']['message']}"

@pytest.mark.smoketest
def test_collection_exists(openeo_test_results):
    assert openeo_test_results['collection_exists']['status'] == 'PASS', \
        f"Collection missing: {openeo_test_results['collection_exists']['message']}"

@pytest.mark.smoketest
def test_list_processes(openeo_test_results):
    assert openeo_test_results['list_processes']['status'] == 'PASS', \
        f"Processes listing failed: {openeo_test_results['list_processes']['message']}"

@pytest.mark.smoketest
def test_process_execution(openeo_test_results):
    assert openeo_test_results['process_execution']['status'] == 'PASS', \
        f"Process execution failed: {openeo_test_results['process_execution']['message']}"

@pytest.mark.smoketest
def test_data_loading(openeo_test_results):
    assert openeo_test_results['data_loading']['status'] == 'PASS', \
        f"Data loading failed: {openeo_test_results['data_loading']['message']}"

@pytest.mark.smoketest
def test_raster_download(openeo_test_results):
    assert openeo_test_results['raster_download']['status'] == 'PASS', \
        f"Raster download failed: {openeo_test_results['raster_download']['message']}"

@pytest.mark.smoketest
def test_raster_open(openeo_test_results):
    assert openeo_test_results['raster_open']['status'] == 'PASS', \
        f"Raster open failed: {openeo_test_results['raster_open']['message']}"

@pytest.mark.smoketest
def test_band_math(openeo_test_results):
    assert openeo_test_results['band_math']['status'] == 'PASS', \
        f"Band math failed: {openeo_test_results['band_math']['message']}"

@pytest.mark.smoketest
def test_nc_download(openeo_test_results):
    assert openeo_test_results['nc_download']['status'] == 'PASS', \
        f"NetCDF download failed: {openeo_test_results['nc_download']['message']}"

@pytest.mark.smoketest
def test_xarray_load_dataset(openeo_test_results):
    assert openeo_test_results['xarray_load_dataset']['status'] == 'PASS', \
        f"xarray dataset loading failed: {openeo_test_results['xarray_load_dataset']['message']}"

@pytest.mark.smoketest
def test_plot_figure(openeo_test_results):
    assert openeo_test_results['plot_figure']['status'] == 'PASS', \
        f"Figure plotting failed: {openeo_test_results['plot_figure']['message']}"
