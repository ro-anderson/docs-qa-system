.PHONY: build run-embedder run-embedder-debug run-chat-cli run-chat-cli-debug clean docker-clean help

SHELL=/bin/bash

# Check if 'docker compose' is available, otherwise fall back to 'docker-compose'
ifeq ($(shell docker compose version 2>/dev/null),)
  DOCKER_COMPOSE := docker-compose
else
  DOCKER_COMPOSE := docker compose
endif

## Build the Docker images
build:
	$(DOCKER_COMPOSE) build

## Build (if needed) and run the batch embedder in Docker
run-embedder: build
	$(DOCKER_COMPOSE) up batch_embedder

## Build (if needed) and run the batch embedder in debug mode (bash shell)
run-embedder-debug: build
	$(DOCKER_COMPOSE) run --rm batch_embedder-bash

## Build (if needed) and run the chat CLI in Docker (interactive)
run-chat-cli: build
	$(DOCKER_COMPOSE) run --rm chat_cli

## Build (if needed) and run the chat CLI in debug mode (bash shell)
run-chat-cli-debug: build
	$(DOCKER_COMPOSE) run --rm chat_cli-bash

## Remove Python cache files
clean:
	find . -name "__pycache__" -type d -exec rm -r {} \+

## Remove Docker containers, networks, and volumes
docker-clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans

## Display help information
help:
	@echo "Available commands:"
	@echo "  make build              - Build the Docker images"
	@echo "  make run-embedder       - Build (if needed) and run the batch embedder in Docker"
	@echo "  make run-embedder-debug - Build (if needed) and run the batch embedder in debug mode"
	@echo "  make run-chat-cli        - Build (if needed) and run the chat CLI in Docker (interactive)"
	@echo "  make run-chat-cli-debug  - Build (if needed) and run the chat CLI in debug mode"
	@echo "  make clean              - Remove Python cache files"
	@echo "  make docker-clean       - Remove Docker containers, networks, and volumes"
	@echo "  make help               - Display this help information"

# Default target
.DEFAULT_GOAL := help
