import os
import sys

from lib import (
    ENV_VAR_INTERNAL_MONGO_CONNECTION_URL,
    ENV_VAR_MONGO_DB,
    ENV_VAR_MONGO_HOST,
    ENV_VAR_MONGO_TECHNICAL_PASSWORD,
    ENV_VAR_MONGO_TECHNICAL_USERNAME,
)
from testcontainers.mongodb import MongoDbContainer

ENV_KEY_TEST_COLLECTION_NAME: str = os.getenv("TEST_COLLECTION_NAME", "test_content")


def sync(mongo_container: MongoDbContainer) -> MongoDbContainer:
    env = mongo_container.env
    for key, value in env.items():
        print("env from container (%s, %s)" % (key, value))
    keys = [
        ENV_VAR_MONGO_DB,
        ENV_VAR_MONGO_TECHNICAL_USERNAME,
        ENV_VAR_MONGO_TECHNICAL_PASSWORD,
    ]
    for index, key in enumerate(keys):
        value = env.get(key)
        if value is not None:
            os.environ[key] = value
        else:
            print("None value provided for key %s" % key, file=sys.stderr)
    os.environ[ENV_VAR_MONGO_HOST] = "%s:%s" % (
        "localhost",
        mongo_container.port_to_expose,
    )
    os.environ[
        ENV_VAR_INTERNAL_MONGO_CONNECTION_URL
    ] = mongo_container.get_connection_url()
    return mongo_container
