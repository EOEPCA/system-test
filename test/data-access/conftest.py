import pytest


@pytest.fixture(scope='session')
def raster_endpoint(EOAPI):
    return f"{EOAPI}/raster"

@pytest.fixture(scope='session')
def vector_endpoint(EOAPI):
    return f"{EOAPI}/vector"

@pytest.fixture(scope='session')
def stac_endpoint(EOAPI):
    return f"{EOAPI}/stac"