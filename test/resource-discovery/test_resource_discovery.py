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
def resource_discovery_test_results(tmp_path_factory):
    temp_output_dir = tmp_path_factory.mktemp('resource_discovery_test')
    output_notebook = temp_output_dir / 'resource-discovery-output.ipynb'
    executed_notebook = temp_output_dir / 'resource-discovery-executed.ipynb'
    log_output_file = temp_output_dir / 'resource-discovery_log.json'

    notebook_path_env = os.getenv("NOTEBOOK_PATH")
    assert notebook_path_env, (
        "NOTEBOOK_PATH must be set to the deployment-guide 'notebooks/examples' directory"
    )
    notebook_repo_path = Path(notebook_path_env) / 'resource-discovery'

    # platform_domain, resource_discovery_enable_iam etc. are left to the notebook's
    # own defaults, derived from `load_eoepca_state()` - only the IAM auth method is
    # forced, since device-code-flow needs an interactive login.
    params = {
        'iam_auth_method': 'scripted',
        'log_output_file': str(log_output_file),
    }

    input_notebook_path = notebook_repo_path / 'resource-discovery.ipynb'

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
@pytest.mark.resource_discovery
def test_endpoints_healthy(resource_discovery_test_results):
    assert resource_discovery_test_results['endpoints_healthy']['status'] == 'PASS', \
        f"Endpoint health check failed: {resource_discovery_test_results['endpoints_healthy']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_csw_capabilities(resource_discovery_test_results):
    assert resource_discovery_test_results['csw_capabilities']['status'] == 'PASS', \
        f"CSW capabilities check failed: {resource_discovery_test_results['csw_capabilities']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_csw_getrecords(resource_discovery_test_results):
    assert resource_discovery_test_results['csw_getrecords']['status'] == 'PASS', \
        f"CSW GetRecords failed: {resource_discovery_test_results['csw_getrecords']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_opensearch_search(resource_discovery_test_results):
    assert resource_discovery_test_results['opensearch_search']['status'] == 'PASS', \
        f"OpenSearch search failed: {resource_discovery_test_results['opensearch_search']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_ogc_records_conformance(resource_discovery_test_results):
    assert resource_discovery_test_results['ogc_records_conformance']['status'] == 'PASS', \
        f"OGC API Records conformance check failed: {resource_discovery_test_results['ogc_records_conformance']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_ogc_records_list(resource_discovery_test_results):
    assert resource_discovery_test_results['ogc_records_list']['status'] == 'PASS', \
        f"OGC API Records listing failed: {resource_discovery_test_results['ogc_records_list']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_ogc_records_items(resource_discovery_test_results):
    assert resource_discovery_test_results['ogc_records_items']['status'] == 'PASS', \
        f"OGC API Records item listing failed: {resource_discovery_test_results['ogc_records_items']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_stac_search(resource_discovery_test_results):
    assert resource_discovery_test_results['stac_search']['status'] == 'PASS', \
        f"STAC search failed: {resource_discovery_test_results['stac_search']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_unauthenticated_write_rejected(resource_discovery_test_results):
    assert resource_discovery_test_results['unauthenticated_write_rejected']['status'] == 'PASS', \
        f"Unauthenticated write check failed: {resource_discovery_test_results['unauthenticated_write_rejected']['message']}"

@pytest.mark.smoketest
@pytest.mark.resource_discovery
def test_transactional_write(resource_discovery_test_results):
    # Known to currently fail: the shared iam-opa/iam-policies bundle's util.rego hardcodes
    # its JWKS lookup at http://iam-keycloak/..., which doesn't resolve on this cluster (the
    # real service is iam-keycloak-operator-service). Every OPA-gated route across every BB
    # 403s regardless of the caller's token/role until that's fixed - not specific to this BB.
    assert resource_discovery_test_results['transactional_write']['status'] == 'PASS', \
        f"Transactional write failed: {resource_discovery_test_results['transactional_write']['message']}"
