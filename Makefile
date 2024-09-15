install-hooks:
	pre-commit install

format-lint:
	poetry run pre-commit run --all-files

# dev

make-env:
	cp config/.env.template config/.env

build:
	docker build . -t product_api:latest -f docker/dockerfile

create-network-docker:
	docker network create back-tier

up-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

up-dev-detach:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

env-export:
	export $(cat config/.env) > /dev/null 2>&1

version:
	@poetry version $(v)
	@git add pyproject.toml
	@git commit -m "v$$(poetry version -s)"
	@git tag v$$(poetry version -s)
	@git push
	@git push --tags
	@poetry version

# migrations

makemigration-docker:
	docker compose exec product_api bash -c 'PYTHONPATH=app alembic --config "/app/alembic.ini" upgrade head'

migrate-docker:
	docker compose exec product_api bash -c 'PYTHONPATH=app alembic --config "/app/alembic.ini" upgrade head'

# Tests

end_to_end_tests:
	poetry run pytest -s tests/end_to_end

tests: end_to_end_tests 
