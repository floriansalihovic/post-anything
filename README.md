# Simply post anything!

## Setup anything!

Required components for building and running:

- [Docker](https://www.docker.com) for managing applications
- [Python Poetry](https://python-poetry.org) for managing project specific dependencies and so much other goodness
- [pyenv](https://github.com/pyenv/pyenv#readme) for managing local python installations

### Environment Variables

The API may read environment variables from the system, but also falls back on defaults:
| Name | Default Value | Comment |
|------|---------------|---------|
| `INTERNAL_MONGO_CONNECTION_URL` | - | used for testcontainers |
| `MONGO_TECHNICAL_USER_USERNAME` | `admin` | setup of technical user recommended ([issue#2](https://github.com/floriansalihovic/post-anything/issues/2)) |
| `MONGO_TECHNICAL_USER_PASSWORD` | `admin` | setup of technical user recommended ([issue#2](https://github.com/floriansalihovic/post-anything/issues/2)) |
| `MONGO_HOST` | `localhost` | |
| `MONGO_PORT` | `27017` | |
| `MONGO_COLLECTION` | `content` | the collection the technical database user needs write access to |
| `MONGO_AUTH_SOURCE` | `admin` | the authentication authority |
 
## Run everything!

Run the database:
```shell
make docker-compose-up
```

Run the containerized HTTP endpoint:
```shell
make docker-build-development docker-run-and-attach
```

Once the container was build, running it by
```shell
make docker-run-and-attach
```
is totally sufficient.

## Post anything!

An example cURL command like:
```shell
curl --request POST \
  --url http://localhost:8000/periodictable/reactivenonmetals/hydrogen \
  --header 'Content-Type: application/json' \
  --data '{ "state":"gas", "weight": 1.008, "energy_levels": 1, "electronegativity":2.20 }'

```
should return anything like
```json
{
  "resource_path": "periodictable/reactivenonmetals/hydrogen1",
  "electronegativity": 2.2,
  "energy_levels": 1,
  "metadata:created": "2021-06-14T18:38:03.933000",
  "metadata:updated": "2021-06-14T18:38:03.933000",
  "state": "gas",
  "weight": 1.008
}
```
The response body will be indented.

## Test everything!

```shell
# automatic path resolution has some issues:
#   - https://github.com/floriansalihovic/post-anything/issues/4
export PYTHONPATH=src:$PYTHONPATH
poetry run pytest
```

## Lint everything!

Running them manually:

```shell
poetry run pre-commit
```
