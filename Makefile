BIND_PORT ?= 8000
BIND_HOST ?= localhost

.PHONY: help
help:  ## Print this help message
	grep -E '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: local-setup
local-setup:  ## Setup local postgres database
	docker compose up -d db

.PHONY: up
up: local-setup  ## Run FastAPI development server
	uv run alembic upgrade head
	uv run uvicorn app.main:app --reload --host $(BIND_HOST) --port $(BIND_PORT)

.PHONY: run
run: up  ## Alias for `up`

.PHONY: down
down:  ## Stop all services
	docker compose down

.PHONY: test
test: local-setup  ## Run unit tests
	uv run pytest .

.PHONY: build
build:  ## Build Docker image
	docker compose build

.PHONY: start
start:  ## Start all services (db + app + nginx)
	docker compose up --build -d
