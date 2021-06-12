include .env.local

.PHONY: docker-build-development
docker-build-development:
	docker build --build-arg POETRY_VERSION=1.1.6 --build-arg DEVELOPMENT_ENV=local -t $(VENDOR_NAME)/$(IMAGE_NAME)-$(IMAGE_VERSION) .

.PHONY: docker-build-production
docker-build-production:
	docker build --build-arg POETRY_VERSION=1.1.6 --build-arg DEVELOPMENT_ENV=production -t $(VENDOR_NAME)/$(IMAGE_NAME)-$(IMAGE_VERSION) .

.PHONY: docker-run
docker-run:
	docker run -d --env-file=./.env.local -p 8000:8000 --name $(IMAGE_NAME) $(VENDOR_NAME)/$(IMAGE_NAME)-$(IMAGE_VERSION)

.PHONY: docker-connect
docker-connect:
	docker network connect $(DOCKER_COMPOSE_NETWORK_NAME) $(IMAGE_NAME)

.PHONY: docker-attach
docker-attach:
	docker attach $(IMAGE_NAME)

.PHONY: docker-stop
docker-stop:
	docker stop $(IMAGE_NAME)

.PHONY: docker-rm
docker-rm:
	docker rm $(IMAGE_NAME)

.PHONY: docker-rmi
docker-rmi:
	docker rmi $(VENDOR_NAME)/$(IMAGE_NAME)-$(IMAGE_VERSION)

.PHONY: docker-run-and-attach
docker-run-and-attach: docker-run docker-connect docker-attach

.PHONY: docker-compose-rebuild
docker-compose-rebuild:
	docker stop "$(MONGO_CONTAINER_NAME)";\
	docker rm "$(MONGO_CONTAINER_NAME)";\
	rm -rf ./.volumes;\
	mkdir -p ./.volumes/mongodb/data/db;\
	docker compose up

.PHONY: docker-compose-up
docker-compose-up:
	mkdir -p ./.volumes/mongodb/data/db;\
	docker compose up;

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: create-hydrogen
create-hydrogen:
	curl --request POST \
	  --url http://localhost:8000/periodictable/reactivenonmetals/hydrogen \
	  --header 'Content-Type: application/json' \
	  --data '{"state":"gas", "weight": 1.008,"energy_levels": 1,"electronegativity":2.20}'
