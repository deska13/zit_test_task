import pytest
from fastapi import status


@pytest.mark.parametrize(
    "count, page, filters, product_types, expected_status, expected_response",
    [
        (
            5,
            0,
            {},
            [],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            None,
        ),
        (
            5000,
            500,
            {},
            [],
            status.HTTP_200_OK,
            {"result": [], "total": 0, "total_page": 0},
        ),
        (
            10,
            1,
            {},
            [{"name": "Books"}],
            status.HTTP_200_OK,
            {"result": [{"name": "Books"}], "total": 1, "total_page": 1},
        ),
        (
            10,
            1,
            {"name": "Electronics"},
            [{"name": "Electronics"}],
            status.HTTP_200_OK,
            {"result": [{"name": "Electronics"}], "total": 1, "total_page": 1},
        ),
        (
            5,
            1,
            {},
            [],
            status.HTTP_200_OK,
            {
                "result": [{"name": "Books"}, {"name": "Electronics"}],
                "total": 2,
                "total_page": 1,
            },
        ),
        (
            1,
            1,
            {},
            [],
            status.HTTP_200_OK,
            {
                "result": [{"name": "Books"}],
                "total": 2,
                "total_page": 2,
            },
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
        (
            5001,
            1,
            {},
            [],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            None,
        ),
        (
            10,
            501,
            {},
            [],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            None,
        ),
    ],
)
def test_get_product_types(
    count,
    page,
    filters,
    product_types,
    expected_status,
    expected_response,
    client,
):
    for product_type in product_types:
        client.post("api/v1/product_types", json=product_type)

    response = client.get(
        "api/v1/product_types",
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
