import pytest
import requests


@pytest.mark.smoketest
def test_stac_api(stac_endpoint, test_user_access_token):
    headers = {"Authorization": f"Bearer {test_user_access_token}"}

    # ping
    response = requests.get(f"{stac_endpoint}/_mgmt/ping")
    assert response.ok, "STAC API ping failed"
    assert response.json()["message"] == "PONG", "Unexpected ping response"

    # viewer
    assert (
        requests.get(f"{stac_endpoint}/index.html").status_code == 404
    )

    # collections
    resp = requests.get(f"{stac_endpoint}/collections")
    assert resp.status_code == 200
    collections = resp.json()["collections"]
    assert len(collections) > 0
    ids = [c["id"] for c in collections]
    assert "noaa-emergency-response" in ids

    # items
    resp = requests.get(f"{stac_endpoint}/collections/noaa-emergency-response/items")
    assert resp.status_code == 200
    items = resp.json()["features"]
    assert len(items) == 10

    # item
    resp = requests.get(
        f"{stac_endpoint}/collections/noaa-emergency-response/items/20200307aC0853300w361200"
    )
    assert resp.status_code == 200
    item = resp.json()
    assert item["id"] == "20200307aC0853300w361200"


@pytest.mark.smoketest
def test_stac_to_raster(stac_endpoint):
    # tilejson
    resp = requests.get(
        f"{stac_endpoint}/collections/noaa-emergency-response/items/20200307aC0853300w361200/tilejson.json",
        params={"assets": "cog"},
    )
    assert resp.status_code == 404

    # viewer
    resp = requests.get(
        f"{stac_endpoint}/collections/noaa-emergency-response/items/20200307aC0853300w361200/viewer",
        params={"assets": "cog"},
    )
    assert resp.status_code == 404
