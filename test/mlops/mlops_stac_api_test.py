import pytest
import requests

@pytest.mark.smoketest
def test_stac_collections_endpoint(mlops_config_api_endpoint):
    stac_api = f"{mlops_config_api_endpoint}/stac/collections"
    response = requests.get(stac_api)
    assert response.ok, "STAC api not responding"
    data = response.json()
    collections = data["collections"]
    assert isinstance(collections, list), f" STAC API not responding"
    for collection in collections:
        collection_resp = requests.get(f"{stac_api}/{collection['id']}")
        assert collection_resp.ok, f"STAC API about collection: {collection_resp} not responding"


@pytest.mark.smoketest
def test_stac_collections_items_endpoint(mlops_config_api_endpoint):
    stac_api = f"{mlops_config_api_endpoint}/stac/collections"
    response = requests.get(stac_api)
    collections =  response.json()["collections"]
    for item in collections:
        response_item = requests.get(f"{stac_api}/{item['id']}/items")
        assert response_item.ok, f"STAC API about collection items not responding"


