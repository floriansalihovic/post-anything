import pytest

PROP_NAME_RESOURCE_PATH = "resource_path"


@pytest.fixture
def document_filter():
    return {PROP_NAME_RESOURCE_PATH: "periodictable/reactivenonmetals/hydrogen"}


@pytest.fixture
def hydrogen_document():
    return {
        "state": "gas",
        "weight": 1.008,
        "energy_levels": 1,
        "electronegativity": 2.20,
    }
