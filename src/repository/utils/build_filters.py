import logging
from typing import Any

from sqlalchemy.sql import and_

logger = logging.getLogger(__name__)


def _get_column(entity_type: Any, filter_key: str) -> Any:
    column = getattr(entity_type, filter_key, None)
    if column is None:
        raise ValueError(f"No column {filter_key} in table {entity_type}")
    return column


def build_filters(table: Any, **kwargs: Any) -> list[Any]:
    filters = []
    for key, value in kwargs.items():
        if value is None:
            pass
        elif key.startswith("from_"):
            filters.append(and_(_get_column(table, key[5:]) <= value))
        elif key.startswith("to_"):
            filters.append(and_(_get_column(table, key[3:]) <= value))
        elif isinstance(value, str):
            filters.append(and_(_get_column(table, key).like(value)))
        else:
            filters.append(and_(_get_column(table, key) == value))
    return filters
