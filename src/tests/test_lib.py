import pytest
from fastapi.testclient import TestClient
from lib import (
    KEY_METADATA_CREATED,
    KEY_METADATA_UPDATED,
    create_or_update,
    is_equal,
    new_mongo_client,
    remove_document,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from testcontainers.mongodb import MongoDbContainer
from tests.env import sync
from tests.fixtures import PROP_NAME_RESOURCE_PATH, document_filter, hydrogen_document


@pytest.fixture(scope="function")
def new_mongo_container():
    with MongoDbContainer("mongo:latest") as container:
        yield container


def test_is_equal():
    d1 = dict()
    assert is_equal(d1, d1, [])
    d2 = dict()
    assert is_equal(d1, d2, [])
    d1["value"] = 1
    d2["value"] = 1
    assert is_equal(d1, d2, [])
    d1["value"] = 1
    d2["value"] = 2
    assert not is_equal(d1, d2, [])
    d1["value1"] = 1
    d2["value2"] = 1
    assert not is_equal(d1, d2, [])


def test_document_api(
    new_mongo_container: MongoDbContainer,
    hydrogen_document: dict,
    document_filter: dict,
):
    new_mongo_container.start()
    sync(new_mongo_container)
    with new_mongo_client(new_mongo_container.get_connection_url()) as mongo_client:
        document, was_created = create_or_update(
            mongo_client,
            document_filter,
            hydrogen_document,
        )
        assert was_created
        assert KEY_METADATA_CREATED in document
        assert KEY_METADATA_UPDATED in document
        assert document.get(KEY_METADATA_CREATED) == document.get(KEY_METADATA_UPDATED)

        melting_point = -259.1
        boiling_point = -252.9
        document, was_created = create_or_update(
            mongo_client,
            document_filter,
            {
                **hydrogen_document,
                **{"melting_point": melting_point, "boiling_point": boiling_point},
            },
        )
        assert not was_created
        assert KEY_METADATA_CREATED in document
        assert KEY_METADATA_UPDATED in document
        assert not document.get(KEY_METADATA_CREATED) == document.get(
            KEY_METADATA_UPDATED
        )
        assert melting_point == document.get("melting_point")
        assert boiling_point == document.get("boiling_point")

        document, was_deleted = remove_document(mongo_client, document_filter)
        assert document is not None
        assert was_deleted
        document, was_deleted = remove_document(mongo_client, document_filter)
        assert document is None
        assert not was_deleted


def test_http_api(
    new_mongo_container: MongoDbContainer,
    hydrogen_document: dict,
    document_filter: dict,
):
    resource_path = f"/{document_filter.get(PROP_NAME_RESOURCE_PATH)}"
    new_mongo_container.start()
    sync(new_mongo_container)
    # load main after environment was updated
    # with the values from the
    from main import api

    test_client = TestClient(api)
    response = test_client.get(resource_path)
    assert HTTP_404_NOT_FOUND == response.status_code

    response = test_client.post(resource_path, json=hydrogen_document)
    assert HTTP_201_CREATED == response.status_code
    assert PROP_NAME_RESOURCE_PATH in response.json()

    test_client = TestClient(api)
    response = test_client.get(resource_path)
    assert HTTP_200_OK == response.status_code

    response = test_client.put(resource_path, json=hydrogen_document)
    assert HTTP_200_OK == response.status_code
    assert PROP_NAME_RESOURCE_PATH in response.json()

    response = test_client.delete(resource_path)
    assert HTTP_200_OK == response.status_code
    assert PROP_NAME_RESOURCE_PATH in response.json()

    response = test_client.delete(resource_path)
    assert HTTP_204_NO_CONTENT == response.status_code
    assert len(response.content) == 0

    test_client = TestClient(api)
    response = test_client.get(resource_path)
    assert HTTP_404_NOT_FOUND == response.status_code
