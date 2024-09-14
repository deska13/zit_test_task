import os
from typing import AsyncIterator, Generator, Iterator

from alembic.config import main as alembic_main
from async_asgi_testclient import TestClient
from docker.models.containers import Container
from dotenv import load_dotenv
from fastapi import FastAPI
from pytest import fixture
from pytest_asyncio import fixture as async_fixture
from tests.utils.docker_containers.postgres import run_postgres_container

import docker

load_dotenv("config/.env.test")

network_name = os.environ.get("TEST_NETWORK")

test_env = os.environ["TEST_ENV"]


@fixture(scope="session")
def docker_client() -> Generator[docker.DockerClient, None, None]:
    client = docker.from_env()
    yield client
    client.close()


@fixture(scope="session", autouse=True)
def db(
    docker_client: docker.DockerClient,
) -> Generator[tuple[Container, str], None, None]:
    container, ip = run_postgres_container(
        docker_client=docker_client, test_env=test_env, network_name=network_name
    )
    try:
        connection = (
            f"postgresql+asyncpg://postgres:postgres@{ip}:5432/recipe_many_reference"
        )
        from app.infra.core import config

        config.postgres_async_connect = connection
        alembic_main(["--raiseerr", "upgrade", "head"])
        yield container, ip
    finally:
        container.stop()


@async_fixture(scope="session")
async def client(app: FastAPI) -> AsyncIterator[TestClient]:
    async with TestClient(app) as client:
        yield client
