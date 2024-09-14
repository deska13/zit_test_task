import pytest
import schemathesis
from fastapi import FastAPI
from starlette_testclient import TestClient

schemathesis.experimental.OPEN_API_3_1.enable()


@pytest.fixture
def sync_client(app: FastAPI):
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def app_schema(sync_client: TestClient):
    openapi = sync_client.app.openapi()
    return schemathesis.from_dict(openapi)


schema = schemathesis.from_pytest_fixture("app_schema")


@schema.parametrize()
def test_api_stateless(case, sync_client: TestClient):
    case.call_and_validate(session=sync_client, timeout=10)
