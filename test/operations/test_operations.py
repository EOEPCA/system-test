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
def operations_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('operations_test')
    output_notebook = temp_output_dir / 'operations-output.ipynb'
    executed_notebook = temp_output_dir / 'operations-executed.ipynb'
    log_output_file = temp_output_dir / 'operations_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'operations'

    # monitoring_url, alerting_url, operations_enable_iam etc. are left to the notebook's
    # own defaults, derived from load_eoepca_state() - only the output log path is forced.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'operations.ipynb'

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
@pytest.mark.operations
def test_endpoints_healthy(operations_test_results):
    assert operations_test_results['endpoints_healthy']['status'] == 'PASS', \
        f"Endpoint health check failed: {operations_test_results['endpoints_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_grafana_authentication(operations_test_results):
    assert operations_test_results['grafana_authentication']['status'] == 'PASS', \
        f"Grafana authentication failed: {operations_test_results['grafana_authentication']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_keep_authentication(operations_test_results):
    assert operations_test_results['keep_authentication']['status'] == 'PASS', \
        f"Keep authentication failed: {operations_test_results['keep_authentication']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_grafana_datasources(operations_test_results):
    assert operations_test_results['grafana_datasources']['status'] == 'PASS', \
        f"Grafana datasources check failed: {operations_test_results['grafana_datasources']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_prometheus_query(operations_test_results):
    assert operations_test_results['prometheus_query']['status'] == 'PASS', \
        f"Prometheus query failed: {operations_test_results['prometheus_query']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_loki_query(operations_test_results):
    assert operations_test_results['loki_query']['status'] == 'PASS', \
        f"Loki query failed: {operations_test_results['loki_query']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_dashboards_loaded(operations_test_results):
    assert operations_test_results['dashboards_loaded']['status'] == 'PASS', \
        f"Dashboards check failed: {operations_test_results['dashboards_loaded']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_watchdog_alert_in_keep(operations_test_results):
    assert operations_test_results['watchdog_alert_in_keep']['status'] == 'PASS', \
        f"Watchdog alert did not reach Keep: {operations_test_results['watchdog_alert_in_keep']['message']}"

@pytest.mark.smoketest
@pytest.mark.operations
def test_stac_proxy_metrics(operations_test_results):
    assert operations_test_results['stac_proxy_metrics']['status'] == 'PASS', \
        f"Data Access STAC proxy metrics check failed: {operations_test_results['stac_proxy_metrics']['message']}"
