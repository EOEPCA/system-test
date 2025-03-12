import pytest


@pytest.fixture(scope="session")
def raster_endpoint(EOAPI):
    return f"https://{EOAPI}/raster"


@pytest.fixture(scope="session")
def vector_endpoint(EOAPI):
    return f"https://{EOAPI}/vector"


@pytest.fixture(scope="session")
def stac_endpoint(EOAPI):
    return f"https://{EOAPI}/stac"
