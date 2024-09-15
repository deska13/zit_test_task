import pytest
from fastapi import status


@pytest.mark.parametrize(
    "product_type, expected_status, expected_response",
    [
        (
            {"name": "Electronics"},
            status.HTTP_201_CREATED,
            {"name": "Electronics"},
        ),
        (
            {"name": "Books"},
            status.HTTP_201_CREATED,
            {"name": "Books"},
        ),
        (
            {"name": ""},
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
            {"name": "A" * 257},
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
            {"name": "Electronics"},
            status.HTTP_409_CONFLICT,
            {"detail": "Product type already exists"},
        ),
    ],
)
def test_create_product_type(
    product_type,
    expected_status,
    expected_response,
    client,
):
    response = client.post(
        url="api/v1/product_types",
        json=product_type,
    )

    assert response.status_code == expected_status
    if expected_status == status.HTTP_201_CREATED:
        assert response.json()["name"] == expected_response["name"]
    else:
        assert response.json() == expected_response
