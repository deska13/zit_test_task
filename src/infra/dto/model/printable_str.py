"""Printable string type for PostgreSQL."""
import re

from pydantic import AfterValidator, StringConstraints
from typing_extensions import Annotated

MIN_LENGTH = 1
MAX_LENGTH = 256


def check_unprintable_chars(text: str) -> str:
    """Валидация символов на возможность их напечатать.

    Args:
        text (str): Строка.

    Raises:
        TypeError: Ошибка типа данных.

    Returns:
        str: Провалидированная строка.
    """
    regex = re.compile(r"[@_!#$%^&*()<>?/\\\|}{~:[\]]")
    assert text.isprintable(), "Строка содержит невыводимые символы"
    assert not regex.search(
        text
    ), f"Строка содержит не поддеживаемый символ {regex.pattern}"
    return text


PrintableStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
    ),
    AfterValidator(check_unprintable_chars),
]
