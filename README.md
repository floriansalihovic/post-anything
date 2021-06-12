# Simply post anything!

## Setup anything!

Required components for building and running:

- [Docker](https://www.docker.com) for managing applications
- [Python Poetry](https://python-poetry.org) for managing project specific dependencies and so much other goodness
- [pyenv](https://github.com/pyenv/pyenv#readme) for managing local python installations

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
  --data '{
	"state":"gas",
	"weight": 1.008,
	"energy_levels": 1,
	"electronegativity":2.20 }'

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
The response body will most likely not be indented.

## Test everything!

```shell
poetry run pytest
```

## Lint everything!

Running them manually:

```shell
poetry run pre-commit
```
