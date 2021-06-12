import logging
import sys
from datetime import datetime
from os import environ, getenv
from typing import Optional, Tuple

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import DeleteResult, UpdateResult

ENV_VAR_NAME_INTERNAL_MONGO_CONNECTION_URL = "INTERNAL_MONGO_CONNECTION_URL"
ENV_VAR_NAME_MONGO_TECHNICAL_USERNAME = "MONGO_INITDB_ROOT_USERNAME"
ENV_VAR_NAME_MONGO_TECHNICAL_PASSWORD = "MONGO_INITDB_ROOT_USERNAME"
ENV_VAR_NAME_MONGO_HOST = "MONGO_HOST"
ENV_VAR_NAME_MONGO_PORT = "27017"
ENV_VAR_NAME_MONGO_DB = "MONGO_DB"
ENV_VAR_NAME_COLLECTION = "MONGO_COLLECTION"
ENV_VAR_NAME_MONGO_AUTH_SOURCE = "MONGO_AUTH_SOURCE"
KEY_DEFAULT_COLLECTION_NAME = "content_root"
KEY_DEFAULT_DB_NAME = "mongo_local_test"
KEY_METADATA_CREATED = "metadata:created"
KEY_METADATA_UPDATED = "metadata:updated"
UNEXPOSED_KEYS = ["_id"]


def init_logging(name: str = None, level: int = logging.DEBUG):
    if name:
        logger_ = logging.getLogger(name)
    else:
        logger_ = logging.getLogger()
    logger_.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger_.addHandler(handler)
    return logger_


def new_mongo_client(connection_url: str = None) -> MongoClient:
    if connection_url:
        print(f"new_mongo_client::connection_url: {connection_url}")
        return MongoClient(connection_url)
    if ENV_VAR_NAME_INTERNAL_MONGO_CONNECTION_URL in environ:
        print(
            f"new_mongo_client::{ENV_VAR_NAME_INTERNAL_MONGO_CONNECTION_URL}:"
            f"{environ.get(ENV_VAR_NAME_INTERNAL_MONGO_CONNECTION_URL)}"
        )
        return MongoClient(environ.get(ENV_VAR_NAME_INTERNAL_MONGO_CONNECTION_URL))
    username = getenv(ENV_VAR_NAME_MONGO_TECHNICAL_USERNAME, "admin")
    password = getenv(ENV_VAR_NAME_MONGO_TECHNICAL_PASSWORD, "admin")
    host = getenv(ENV_VAR_NAME_MONGO_HOST, "localhost")
    port = getenv(ENV_VAR_NAME_MONGO_PORT, "27017")
    auth_source = getenv(ENV_VAR_NAME_MONGO_AUTH_SOURCE, "admin")
    uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}"
    print(f"new_mongo_client::uri: {uri}")
    return MongoClient(uri)


logger = init_logging(__name__)


def get_collection(client: MongoClient) -> Collection:
    return client[getenv(ENV_VAR_NAME_MONGO_DB, KEY_DEFAULT_DB_NAME)][
        getenv(ENV_VAR_NAME_COLLECTION, KEY_DEFAULT_COLLECTION_NAME)
    ]


def is_equal(d1: dict, d2: dict, excluded_keys: list) -> bool:
    if d1 is d2:
        return True
    d1_ = remove_keys(d1, excluded_keys)
    d2_ = remove_keys(d2, excluded_keys)
    if d1_ is None or d2_ is None or d1_.keys() != d2_.keys():
        return False
    for key, value in d1_.items():
        if not value == d2_.get(key):
            return False
    return True


def remove_keys(document: Optional[dict], excluding_keys: list) -> Optional[dict]:
    return (
        None
        if document is None
        else {
            key: value for key, value in document.items() if key not in excluding_keys
        }
    )


def find_in_collection_by(client: MongoClient, predicate: dict) -> Optional[dict]:
    return remove_keys(get_collection(client).find_one(predicate), UNEXPOSED_KEYS)


def create_or_update(
    client: MongoClient,
    document_filter: dict,
    document_body: dict,
) -> Tuple[dict, bool]:
    collection_: Collection = get_collection(client)
    original_document: dict = collection_.find_one(document_filter)
    updated_document = {**document_body, **document_filter}
    if is_equal(
        original_document,
        updated_document,
        ["_id", KEY_METADATA_CREATED, KEY_METADATA_UPDATED],
    ):
        return remove_keys(original_document, UNEXPOSED_KEYS), False

    updated_document.update({KEY_METADATA_UPDATED: datetime.utcnow()})
    result: UpdateResult = collection_.update_one(
        document_filter,
        {
            "$set": remove_keys(updated_document, [KEY_METADATA_CREATED]),
            "$setOnInsert": {
                KEY_METADATA_CREATED: updated_document.get(KEY_METADATA_UPDATED)
            },
        },
        upsert=True,
    )
    return (
        remove_keys(collection_.find_one(document_filter), UNEXPOSED_KEYS),
        result.modified_count == 0,
    )


def remove_document(client: MongoClient, document_filter: dict) -> Tuple[dict, bool]:
    document: dict = find_in_collection_by(client, document_filter)
    result: DeleteResult = get_collection(client).delete_one(document_filter)
    return remove_keys(document, UNEXPOSED_KEYS), result.deleted_count > 0
