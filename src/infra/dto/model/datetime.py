"""Datetime type for PostgreSQL."""
from datetime import datetime, timedelta
from typing import Annotated

from pydantic import AfterValidator


def check_timezone_utcoffset_range(datetime_for_parse: datetime) -> datetime:
    utc_offset = datetime_for_parse.utcoffset()
    from_utc_offset_hours = 12
    to_utc_offset_hours = 13
    assert utc_offset is not None and (
        utc_offset < timedelta(days=-1, hours=from_utc_offset_hours)
        or utc_offset > timedelta(hours=to_utc_offset_hours)
    ), "Часовой пояс должен быть задан с -12:00 по +13:00"
    return datetime_for_parse


Datetime = Annotated[datetime, AfterValidator(check_timezone_utcoffset_range)]
