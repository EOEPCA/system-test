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
def application_quality_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('application_quality_test')
    output_notebook = temp_output_dir / 'application-quality-output.ipynb'
    executed_notebook = temp_output_dir / 'application-quality-executed.ipynb'
    log_output_file = temp_output_dir / 'application-quality_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'application-quality'

    # platform_domain, application_quality_enable_iam etc. are left to the notebook's
    # own defaults, derived from `load_eoepca_state()`.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'application-quality.ipynb'

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
@pytest.mark.application_quality
def test_endpoints_healthy(application_quality_test_results):
    assert application_quality_test_results['endpoints_healthy']['status'] == 'PASS', \
        f"Endpoint health check failed: {application_quality_test_results['endpoints_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.application_quality
def test_list_tools(application_quality_test_results):
    assert application_quality_test_results['list_tools']['status'] == 'PASS', \
        f"Tools listing failed: {application_quality_test_results['list_tools']['message']}"

@pytest.mark.smoketest
@pytest.mark.application_quality
def test_list_tags(application_quality_test_results):
    assert application_quality_test_results['list_tags']['status'] == 'PASS', \
        f"Tags listing failed: {application_quality_test_results['list_tags']['message']}"

@pytest.mark.smoketest
@pytest.mark.application_quality
def test_authentication(application_quality_test_results):
    assert application_quality_test_results['authentication']['status'] == 'PASS', \
        f"Authentication failed: {application_quality_test_results['authentication']['message']}"

@pytest.mark.smoketest
@pytest.mark.application_quality
def test_list_pipelines(application_quality_test_results):
    assert application_quality_test_results['list_pipelines']['status'] == 'PASS', \
        f"Pipeline listing failed: {application_quality_test_results['list_pipelines']['message']}"

@pytest.mark.smoketest
@pytest.mark.application_quality
def test_create_pipeline(application_quality_test_results):
    assert application_quality_test_results['create_pipeline']['status'] == 'PASS', \
        f"Pipeline creation failed: {application_quality_test_results['create_pipeline']['message']}"

@pytest.mark.smoketest
@pytest.mark.application_quality
def test_trigger_pipeline_run(application_quality_test_results):
    assert application_quality_test_results['trigger_pipeline_run']['status'] == 'PASS', \
        f"Triggering the pipeline run failed: {application_quality_test_results['trigger_pipeline_run']['message']}"

@pytest.mark.smoketest
@pytest.mark.application_quality
def test_pipeline_execution(application_quality_test_results):
    # Known to currently fail: the shipped image's vendored pycalrissian has per-run
    # namespace RBAC role creation disabled ("create role %s ... DISABLED" in
    # celery_err.log), so Calrissian's own job monitor can never list/get pods in the
    # namespace it just created and the run never reaches a terminal status. This is a
    # bug in the shipped application-quality image, not the deployment guide or notebook.
    assert application_quality_test_results['pipeline_execution']['status'] == 'PASS', \
        f"Pipeline execution failed: {application_quality_test_results['pipeline_execution']['message']}"
