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
def workspace_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('workspace_test')
    output_notebook = temp_output_dir / 'workspace-output.ipynb'
    executed_notebook = temp_output_dir / 'workspace-executed.ipynb'
    log_output_file = temp_output_dir / 'workspace_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'workspace'

    # demo_user, workspace_api_client_id etc. are left to the notebook's own
    # defaults, derived from load_eoepca_state() - only the output log path is forced.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'workspace.ipynb'

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
@pytest.mark.workspace
def test_workspace_api_reachable(workspace_test_results):
    assert workspace_test_results['workspace_api_reachable']['status'] == 'PASS', \
        f"Workspace API not reachable: {workspace_test_results['workspace_api_reachable']['message']}"

@pytest.mark.smoketest
@pytest.mark.workspace
def test_create_workspace(workspace_test_results):
    assert workspace_test_results['create_workspace']['status'] == 'PASS', \
        f"Workspace creation failed: {workspace_test_results['create_workspace']['message']}"

@pytest.mark.smoketest
@pytest.mark.workspace
def test_workspace_provisioned(workspace_test_results):
    assert workspace_test_results['workspace_provisioned']['status'] == 'PASS', \
        f"Workspace did not become ready: {workspace_test_results['workspace_provisioned']['message']}"

@pytest.mark.smoketest
@pytest.mark.workspace
def test_s3_bucket_access(workspace_test_results):
    assert workspace_test_results['s3_bucket_access']['status'] == 'PASS', \
        f"S3 bucket access failed: {workspace_test_results['s3_bucket_access']['message']}"

@pytest.mark.smoketest
@pytest.mark.workspace
def test_datalab_session_started(workspace_test_results):
    assert workspace_test_results['datalab_session_started']['status'] == 'PASS', \
        f"Datalab session did not start: {workspace_test_results['datalab_session_started']['message']}"

@pytest.mark.smoketest
@pytest.mark.workspace
def test_workspace_deleted(workspace_test_results):
    assert workspace_test_results['workspace_deleted']['status'] == 'PASS', \
        f"Workspace deletion failed: {workspace_test_results['workspace_deleted']['message']}"
