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
def iam_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('iam_test')
    output_notebook = temp_output_dir / 'iam-output.ipynb'
    executed_notebook = temp_output_dir / 'iam-executed.ipynb'
    log_output_file = temp_output_dir / 'iam_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'iam'

    # keycloak_host, realm, opa_client_id etc. are left to the notebook's own
    # defaults, derived from `load_eoepca_state()`.
    params = {
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'iam.ipynb'

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
@pytest.mark.iam
def test_oidc_discovery(iam_test_results):
    assert iam_test_results['oidc_discovery']['status'] == 'PASS', \
        f"OIDC discovery failed: {iam_test_results['oidc_discovery']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_uma_discovery(iam_test_results):
    assert iam_test_results['uma_discovery']['status'] == 'PASS', \
        f"UMA discovery failed: {iam_test_results['uma_discovery']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_authenticate(iam_test_results):
    assert iam_test_results['authenticate']['status'] == 'PASS', \
        f"Authentication failed: {iam_test_results['authenticate']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_userinfo(iam_test_results):
    assert iam_test_results['userinfo']['status'] == 'PASS', \
        f"Userinfo request failed: {iam_test_results['userinfo']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_opa_authorized(iam_test_results):
    assert iam_test_results['opa_authorized']['status'] == 'PASS', \
        f"OPA health check failed: {iam_test_results['opa_authorized']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_opa_unauthorized_rejected(iam_test_results):
    assert iam_test_results['opa_unauthorized_rejected']['status'] == 'PASS', \
        f"OPA did not reject an invalid token: {iam_test_results['opa_unauthorized_rejected']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_fine_grained_authorization(iam_test_results):
    assert iam_test_results['fine_grained_authorization']['status'] == 'PASS', \
        f"UMA authorization decision failed: {iam_test_results['fine_grained_authorization']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_fine_grained_authorization_denied(iam_test_results):
    assert iam_test_results['fine_grained_authorization_denied']['status'] == 'PASS', \
        f"UMA authorization decision was not rejected for an unauthenticated caller: {iam_test_results['fine_grained_authorization_denied']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_crossplane_client_provisioned(iam_test_results):
    assert iam_test_results['crossplane_client_provisioned']['status'] == 'PASS', \
        f"Crossplane client provisioning failed: {iam_test_results['crossplane_client_provisioned']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_crossplane_client_token(iam_test_results):
    assert iam_test_results['crossplane_client_token']['status'] == 'PASS', \
        f"Newly provisioned client could not obtain a token: {iam_test_results['crossplane_client_token']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_resource_protection_allowed(iam_test_results):
    assert iam_test_results['resource_protection_allowed']['status'] == 'PASS', \
        f"Group member was not granted access to their own resource: {iam_test_results['resource_protection_allowed']['message']}"

@pytest.mark.smoketest
@pytest.mark.iam
def test_resource_protection_denied(iam_test_results):
    assert iam_test_results['resource_protection_denied']['status'] == 'PASS', \
        f"Non-member was not denied access: {iam_test_results['resource_protection_denied']['message']}"
