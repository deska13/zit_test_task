import pytest
from fastapi import status


@pytest.mark.parametrize(
    "product_input, expected_status, expected_response",
    [
        (
            {"name": "Product A", "product_type": {"name": "Books"}},
            status.HTTP_201_CREATED,
            {"name": "Product A"},
        ),
        (
            {"name": "Product B", "product_type": {"name": "Electronics"}},
            status.HTTP_201_CREATED,
            {"name": "Product B"},
        ),
    ],
)
def test_create_product_type(
    product_input,
    expected_status,
    expected_response,
    client,
):
    created_product_type = client.post(
        "api/v1/product_types",
        json=product_input["product_type"],
    ).json()
    del product_input["product_type"]
    product_input["product_type_id"] = created_product_type["id"]
    response = client.post("api/v1/products", json=product_input)

    assert response.status_code == expected_status
    assert response.json()["name"] == expected_response["name"]
