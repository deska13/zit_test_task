from typing import Generator

import pytest
from httpx import Client
from testcontainers.core.container import DockerContainer
from testcontainers.core.network import Network
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="module", name="network")
def setup_container_network() -> Generator[DockerContainer, None, None]:
    with Network() as network:
        yield network


@pytest.fixture(scope="module", name="db")
def setup_db_container(
    network: Network,
) -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:15-alpine").with_network(
        network=network
    ) as container:
        wait_for_logs(container, "database system is ready to accept connections")
        yield container


@pytest.fixture(scope="module", name="api")
def setup_api_container(
    network: Network,
    db: PostgresContainer,
) -> Generator[DockerContainer, None, None]:
    with DockerContainer(
        "product_api:latest",
    ).with_env(
        "POSTGRES_HOST",
        db.get_wrapped_container().name,
    ).with_env(
        "POSTGRES_DB",
        db.dbname,
    ).with_env(
        "POSTGRES_USER",
        db.username,
    ).with_env(
        "POSTGRES_PASSWORD",
        db.password,
    ).with_exposed_ports(
        8000,
    ).with_network(
        network=network,
    ) as container:
        wait_for_logs(container, "Application startup complete.")
        yield container


@pytest.fixture(scope="module", name="client")
def setup_api_client(
    api: DockerContainer,
) -> Generator[Client, None, None]:
    host = api.get_container_host_ip()
    port = api.get_exposed_port(8000)
    with Client(base_url=f"http://{host}:{port}/") as client:
        yield client
