import pytest
from fastapi import status


@pytest.mark.parametrize(
    "count, page, filters, products, expected_status, expected_response",
    [
        (
            10,
            1,
            {},
            [],
            status.HTTP_200_OK,
            {"result": [], "total": 0, "total_page": 0},
        ),
        (
            50,
            1,
            {"name": "Product 2"},
            [{"name": "Product 2", "product_type": {"name": "Electronics"}}],
            status.HTTP_200_OK,
            {"result": [{"name": "Product 2"}], "total": 1, "total_page": 1},
        ),
        (
            1,
            0,
            {},
            [],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            None,
        ),
        (
            5000,
            1,
            {},
            [],
            status.HTTP_200_OK,
            {"result": [{"name": "Product 2"}], "total": 1, "total_page": 1},
        ),
        (
            5000,
            500,
            {},
            [],
            status.HTTP_200_OK,
            {"result": [], "total": 1, "total_page": 1},
        ),
        (
            0,
            1,
            {},
            [],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            None,
        ),
        (
            10,
            -1,
            {},
            [],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            None,
        ),
    ],
)
def test_get_products(
    count,
    page,
    filters,
    products,
    expected_status,
    expected_response,
    client,
):
    for product in products:
        created_product_type = client.post(
            "api/v1/product_types",
            json=product["product_type"],
        ).json()
        del product["product_type"]
        product["product_type_id"] = str(created_product_type["id"])
        client.post("api/v1/products", json=product)

    response = client.get(
        "api/v1/products",
        params={"count": count, "page": page, **filters},
    )

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        assert data["total"] == expected_response["total"], "total error"
        assert data["total_page"] == expected_response["total_page"], "total page error"
        assert len(data["result"]) == len(
            expected_response["result"]
        ), "len result error"
