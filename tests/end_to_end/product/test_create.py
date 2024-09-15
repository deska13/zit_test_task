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
        (
            {"name": "", "product_type": {"name": "Toys"}},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "name"],
                        "msg": "String should have at least 1 character",
                        "input": "",
                        "ctx": {"min_length": 1},
                    }
                ]
            },
        ),
        (
            {"name": "A" * 257, "product_type": {"name": "Zoo"}},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "type": "string_too_long",
                        "loc": ["body", "name"],
                        "msg": "String should have at most 256 characters",
                        "input": "A" * 257,
                        "ctx": {"max_length": 256},
                    }
                ]
            },
        ),
        (
            {"name": "Product B", "product_type": {"name": "Mobile"}},
            status.HTTP_409_CONFLICT,
            {"detail": "Product already exists"},
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
    if expected_status == status.HTTP_201_CREATED:
        assert response.json()["name"] == expected_response["name"]
    else:
        assert response.json() == expected_response
