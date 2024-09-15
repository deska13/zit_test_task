from uuid import UUID

import pytest
from fastapi import status


@pytest.mark.parametrize(
    "product, expected_status, expected_response",
    [
        (
            {"name": "Product 1", "product_type": {"name": "Books"}},
            status.HTTP_200_OK,
            {"name": "Product 1"},
        ),
        (
            {"name": "Product 2", "product_type": {"name": "Electronics"}},
            status.HTTP_200_OK,
            {"name": "Product 2"},
        ),
    ],
)
def test_get_product_by_id(
    product,
    expected_status,
    expected_response,
    client,
):
    created_product_type = client.post(
        "api/v1/product_types", json=product["product_type"]
    ).json()
    del product["product_type"]
    product["product_type_id"] = str(created_product_type["id"])

    created_product_response = client.post("api/v1/products", json=product)
    created_product = created_product_response.json()
    response = client.get(f"api/v1/products/{created_product['id']}")

    assert response.status_code == expected_status
    data = response.json()
    assert data["name"] == expected_response["name"]


@pytest.mark.parametrize(
    "product_id, expected_status, expected_detail",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174002"),
            status.HTTP_404_NOT_FOUND,
            "Product not found",
        ),
    ],
)
def test_get_product_by_id_error_cases(
    product_id,
    expected_status,
    expected_detail,
    client,
):
    response = client.get(f"api/v1/products/{product_id}")

    assert response.status_code == expected_status
    assert response.json() == {"detail": expected_detail}
