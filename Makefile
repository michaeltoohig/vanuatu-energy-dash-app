# SHELL := /bin/bash
# PWD=$(shell pwd)
COMPOSE_FILE := docker-compose.yml

.PHONY: build
build:
	docker compose --file $(COMPOSE_FILE) build $(c)

.PHONY: up
up:
	docker compose --file $(COMPOSE_FILE) up -d $(c)

.PHONY: restart
restart:
	docker compose --file $(COMPOSE_FILE) restart $(c)

.PHONY: stop
stop:
	docker compose --file $(COMPOSE_FILE) stop $(c)

.PHONY: down
down:
	docker compose --file $(COMPOSE_FILE) down

.PHONY: logs
logs:
	docker compose --file $(COMPOSE_FILE) logs --tail=100 -f $(c)
