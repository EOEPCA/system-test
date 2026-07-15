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
def notification_automation_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('notification_automation_test')
    output_notebook = temp_output_dir / 'notification-automation-output.ipynb'
    executed_notebook = temp_output_dir / 'notification-automation-executed.ipynb'
    log_output_file = temp_output_dir / 'notification-automation_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'notification-automation'

    # platform_domain, webhook_source_url etc. are left to the notebook's own defaults,
    # derived from load_eoepca_state() - only the output log path is forced.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'notification-automation.ipynb'

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
@pytest.mark.notification_automation
def test_endpoints_healthy(notification_automation_test_results):
    assert notification_automation_test_results['endpoints_healthy']['status'] == 'PASS', \
        f"Endpoint health check failed: {notification_automation_test_results['endpoints_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.notification_automation
def test_api_server_source_events(notification_automation_test_results):
    assert notification_automation_test_results['api_server_source_events']['status'] == 'PASS', \
        f"API Server Source event check failed: {notification_automation_test_results['api_server_source_events']['message']}"

@pytest.mark.smoketest
@pytest.mark.notification_automation
def test_webhook_signature_rejected(notification_automation_test_results):
    assert notification_automation_test_results['webhook_signature_rejected']['status'] == 'PASS', \
        f"Webhook signature rejection check failed: {notification_automation_test_results['webhook_signature_rejected']['message']}"

@pytest.mark.smoketest
@pytest.mark.notification_automation
def test_webhook_event_delivered(notification_automation_test_results):
    assert notification_automation_test_results['webhook_event_delivered']['status'] == 'PASS', \
        f"Webhook event delivery check failed: {notification_automation_test_results['webhook_event_delivered']['message']}"
